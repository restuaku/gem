"""SheerID Student Verification Main Program"""
import re
import random
import logging
import httpx
from typing import Dict, Optional, Tuple

import config
from name_generator import NameGenerator, generate_birth_date
from img_generator import generate_image, generate_school_email

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:
    """SheerID Student Identity Verifier"""

    def __init__(self, verification_id: str):
        self.verification_id = verification_id
        self.device_fingerprint = self._generate_device_fingerprint()
        self.http_client = httpx.Client(timeout=30.0)

    def __del__(self):
        if hasattr(self, "http_client"):
            self.http_client.close()

    @staticmethod
    def _generate_device_fingerprint() -> str:
        chars = '0123456789abcdef'
        return ''.join(random.choice(chars) for _ in range(32))

    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL (keep as is)"""
        return url

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def _sheerid_request(
        self, method: str, url: str, body: Optional[Dict] = None
    ) -> Tuple[Dict, int]:
        """Send SheerID API request"""
        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = self.http_client.request(
                method=method, url=url, json=body, headers=headers
            )
            try:
                data = response.json()
            except Exception:
                data = response.text
            return data, response.status_code
        except Exception as e:
            logger.error(f"SheerID request failed: {e}")
            raise

    def _upload_to_s3(self, upload_url: str, img_data: bytes) -> bool:
        """Upload PNG to S3"""
        try:
            headers = {"Content-Type": "image/png"}
            response = self.http_client.put(
                upload_url, content=img_data, headers=headers, timeout=60.0
            )
            return 200 <= response.status_code < 300
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            return False

    def verify(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        birth_date: str = None,
        school_data: dict = None,
    ) -> Dict:
        """Execute verification process"""
        try:
            current_step = "initial"

            # ✅ VALIDASI: school_data WAJIB ada
            if not school_data:
                raise Exception("school_data is required! User must select a school.")

            # Generate random name jika tidak ada
            if not first_name or not last_name:
                name = NameGenerator.generate()
                first_name = name["first_name"]
                last_name = name["last_name"]

            # ✅ AMBIL data school dari parameter
            # Jika dari preset, bisa lookup config.SCHOOLS untuk data lengkap
            # Jika dari search API, langsung pakai data yang ada
            if school_data.get('from_search'):
                # Dari search API, pakai data langsung
                school = {
                    'id': school_data['id'],
                    'idExtended': school_data['idExtended'],
                    'name': school_data['name'],
                    'domain': school_data.get('domain', 'university.edu')
                }
            elif school_data.get('dict_key'):
                # Dari preset, lookup config.SCHOOLS untuk data lengkap
                school = config.SCHOOLS[school_data['dict_key']]
            else:
                # Fallback: pakai data yang ada di school_data
                school = {
                    'id': school_data['id'],
                    'idExtended': school_data['idExtended'],
                    'name': school_data['name'],
                    'domain': school_data.get('domain', 'university.edu')
                }

            # ✅ Generate email dengan domain dari school
            if not email:
                email = generate_school_email(
                    first_name, 
                    last_name, 
                    school['domain']
                )

            if not birth_date:
                birth_date = generate_birth_date()

            logger.info(f"Student info: {first_name} {last_name}")
            logger.info(f"Email: {email}")
            logger.info(f"School: {school['name']}")
            logger.info(f"School Domain: {school['domain']}")
            logger.info(f"Birth date: {birth_date}")
            logger.info(f"Verification ID: {self.verification_id}")

            # Generate student card PNG
            logger.info("Step 1/4: Generating student card PNG...")
            img_data = generate_image(first_name, last_name, str(school['id']))
            file_size = len(img_data)
            logger.info(f"✅ PNG size: {file_size / 1024:.2f}KB")

            # Submit student information
            logger.info("Step 2/4: Submitting student information...")
            step2_body = {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": birth_date,
                "email": email,
                "phoneNumber": "",
                "organization": {
                    "id": school['id'],  # INTEGER dari SheerID API
                    "idExtended": school['idExtended'],  # STRING
                    "name": school['name'],
                },
                "deviceFingerprintHash": self.device_fingerprint,
                "locale": "en-US",
                "metadata": {
                    "marketConsentValue": False,
                    "refererUrl": f"{config.SHEERID_BASE_URL}/verify/{config.PROGRAM_ID}/?verificationId={self.verification_id}",
                    "verificationId": self.verification_id,
                    "flags": '{"collect-info-step-email-first":"default","doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","font-size":"default","include-cvec-field-france-student":"not-labeled-optional"}',
                    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount",
                },
            }

            step2_data, step2_status = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectStudentPersonalInfo",
                step2_body,
            )

            if step2_status != 200:
                raise Exception(f"Step 2 failed (status code {step2_status}): {step2_data}")
            if step2_data.get("currentStep") == "error":
                error_msg = ", ".join(step2_data.get("errorIds", ["Unknown error"]))
                raise Exception(f"Step 2 error: {error_msg}")

            logger.info(f"✅ Step 2 completed: {step2_data.get('currentStep')}")
            current_step = step2_data.get("currentStep", current_step)

            # Skip SSO (if needed)
            if current_step in ["sso", "collectStudentPersonalInfo"]:
                logger.info("Step 3/4: Skipping SSO verification...")
                step3_data, _ = self._sheerid_request(
                    "DELETE",
                    f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso",
                )
                logger.info(f"✅ Step 3 completed: {step3_data.get('currentStep')}")
                current_step = step3_data.get("currentStep", current_step)

            # Upload document and complete submission
            logger.info("Step 4/4: Requesting and uploading document...")
            step4_body = {
                "files": [
                    {"fileName": "student_card.png", "mimeType": "image/png", "fileSize": file_size}
                ]
            }
            step4_data, step4_status = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
                step4_body,
            )
            if not step4_data.get("documents"):
                raise Exception("Failed to get upload URL")

            upload_url = step4_data["documents"][0]["uploadUrl"]
            logger.info("✅ Successfully got upload URL")
            if not self._upload_to_s3(upload_url, img_data):
                raise Exception("S3 upload failed")
            logger.info("✅ Student card uploaded successfully")

            step6_data, _ = self._sheerid_request(
                "POST",
                f"{config.SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload",
            )
            logger.info(f"✅ Document submission completed: {step6_data.get('currentStep')}")
            final_status = step6_data

            # No status polling, return pending review directly
            return {
                "success": True,
                "pending": True,
                "message": "Document submitted, waiting for review",
                "verification_id": self.verification_id,
                "redirect_url": final_status.get("redirectUrl"),
                "status": final_status,
                "student_info": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "birth_date": birth_date,
                    "school_name": school['name']
                }
            }

        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return {"success": False, "message": str(e), "verification_id": self.verification_id}


def main():
    """Main function - Command line interface"""
    import sys

    print("=" * 60)
    print("SheerID Student Verification Tool (Python)")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter SheerID verification URL: ").strip()

    if not url:
        print("❌ Error: No URL provided")
        sys.exit(1)

    verification_id = SheerIDVerifier.parse_verification_id(url)
    if not verification_id:
        print("❌ Error: Invalid verification ID format")
        sys.exit(1)

    print(f"✅ Parsed verification ID: {verification_id}")
    print()

    # ✅ Untuk CLI, user harus pilih school manually
    print("⚠️  Note: school_data required. Use Telegram bot for full functionality.")
    print()

    verifier = SheerIDVerifier(verification_id)
    
    # Example: gunakan school pertama dari config sebagai demo
    first_school_id = list(config.SCHOOLS.keys())[0]
    school_data_demo = {
        'dict_key': first_school_id,
        'id': config.SCHOOLS[first_school_id]['id'],
        'idExtended': config.SCHOOLS[first_school_id]['idExtended'],
        'name': config.SCHOOLS[first_school_id]['name'],
        'domain': config.SCHOOLS[first_school_id]['domain'],
        'from_search': False
    }
    
    result = verifier.verify(school_data=school_data_demo)

    print()
    print("=" * 60)
    print("Verification Result:")
    print("=" * 60)
    print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    print(f"Message: {result['message']}")
    if result.get("redirect_url"):
        print(f"Redirect URL: {result['redirect_url']}")
    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    exit(main())
