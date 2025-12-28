# SheerID 验证配置文件

# SheerID API 配置
PROGRAM_ID = '67c8c14f5f17a83b745e3f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'
ORGSEARCH_API_URL = 'https://orgsearch.sheerid.net/rest/organization/search'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# 学校配置 - Top A+/A US Universities 2026 (SHEERID OFFICIAL IDs)
SCHOOLS = {
    # ===== CALIFORNIA (7) =====
    '2284': {
        'id': 3113,
        'idExtended': '3113',
        'name': 'Stanford University',
        'city': 'Stanford',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'stanford.edu',
        'latitude': 37.4275,
        'longitude': -122.1697
    },
    '2286': {
        'id': 2286,
        'idExtended': '2286',
        'name': 'California Institute of Technology - Caltech',
        'city': 'Pasadena',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'caltech.edu',
        'latitude': 34.1375,
        'longitude': -118.1253
    },
    '2287': {
        'id': 397,
        'idExtended': '397',
        'name': 'University of California, Berkeley',
        'city': 'Berkeley',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'berkeley.edu',
        'latitude': 34.1377,
        'longitude': -118.1253
    },
    '3499': {
        'id': 3491,
        'idExtended': '3491',
        'name': 'University of California-Los Angeles - UCLA',
        'city': 'Los Angeles',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'ucla.edu',
        'latitude': 37.8719,
        'longitude': -122.2585
    },
    '3500': {
        'id': 3500,
        'idExtended': '3500',
        'name': 'University of California, San Diego - UCSD',
        'city': 'La Jolla',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'ucsd.edu',
        'latitude': 32.8801,
        'longitude': -117.2340
    },
    '3501': {
        'id': 3501,
        'idExtended': '3501',
        'name': 'University of California, Irvine - UCI',
        'city': 'Irvine',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'uci.edu',
        'latitude': 33.6403,
        'longitude': -117.8441
    },
    '3502': {
        'id': 3501,
        'idExtended': '3501',
        'name': 'University of California-San Francisco',
        'city': 'Davis',
        'state': 'CA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'ucdavis.edu',
        'latitude': 37.7628,
        'longitude': -122.4578
    },
    # ===== MASSACHUSETTS (4) =====
    '2285': {
        'id': 1953,
        'idExtended': '1953',
        'name': 'Massachusetts Institute of Technology - MIT',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'mit.edu',
        'latitude': 42.3601,
        'longitude': -71.0942
    },
    '2283': {
        'id': 1426,
        'idExtended': '1426',
        'name': 'Harvard University',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'harvard.edu',
        'latitude': 42.3770,
        'longitude': -71.1167
    },
    '3503': {
        'id': 332484,
        'idExtended': '332484',
        'name': 'Tufts University',
        'city': 'Medford',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'tufts.edu',
        'latitude': 42.3385,
        'longitude': -71.0965
    },
    '3504': {
        'id': 274,
        'idExtended': '3504',
        'name': 'Boston College',
        'city': 'Chestnut Hill',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'bc.edu',
        'latitude': 42.3403,
        'longitude': -71.1666
    },
    # ===== CONNECTICUT (1) =====
    '2282': {
        'id': 590759,
        'idExtended': '590759',
        'name': 'Yale University',
        'city': 'New Haven',
        'state': 'CT',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'yale.edu',
        'latitude': 41.3115,
        'longitude': -72.9240
    },
    # ===== NEW JERSEY (1) =====
    '2281': {
        'id': 2626,
        'idExtended': '2626',
        'name': 'Princeton University',
        'city': 'Princeton',
        'state': 'NJ',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'princeton.edu',
        'latitude': 40.3431,
        'longitude': -74.6551
    },
    # ===== NEW YORK (5) =====
    '2280': {
        'id': 698,
        'idExtended': '698',
        'name': 'Columbia University in the City of New York',
        'city': 'New York City',
        'state': 'NY',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'columbia.edu',
        'latitude': 40.8075,
        'longitude': -73.9626
    },
    '2279': {
        'id': 2285,
        'idExtended': '2285',
        'name': 'New York University - NYU',
        'city': 'New York City',
        'state': 'NY',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'nyu.edu',
        'latitude': 40.7295,
        'longitude': -73.9965
    },
    '2278': {
        'id': 751,
        'idExtended': '2278',
        'name': 'Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'cornell.edu',
        'latitude': 42.4534,
        'longitude': -76.4735
    },
    '3505': {
        'id': 3656,
        'idExtended': '36565',
        'name': 'University of Rochester',
        'city': 'Rochester',
        'state': 'NY',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'rochester.edu',
        'latitude': 43.1306,
        'longitude': -77.6260
    },
    '3506': {
        'id': 9026,
        'idExtended': '9026',
        'name': 'Rensselaer Polytechnic Institute',
        'city': 'Troy',
        'state': 'NY',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'rpi.edu',
        'latitude': 42.7302,
        'longitude': -73.6788
    },
    # ===== PENNSYLVANIA (2) =====
    '2277': {
        'id': 3643,
        'idExtended': '3643',
        'name': 'University of Pennsylvania',
        'city': 'Philadelphia',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'upenn.edu',
        'latitude': 39.9490,
        'longitude': -75.1959
    },
    '3507': {
        'id': 445,
        'idExtended': '445',
        'name': 'Carnegie Mellon University',
        'city': 'Pittsburgh',
        'state': 'PA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'cmu.edu',
        'latitude': 40.4428,
        'longitude': -79.9430
    },
    # ===== ILLINOIS (3) =====
    '2276': {
        'id': 3508,
        'idExtended': '3508',
        'name': 'University of Chicago',
        'city': 'Chicago',
        'state': 'IL',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'uchicago.edu',
        'latitude': 41.7880,
        'longitude': -87.5995
    },
    '2275': {
        'id': 2420,
        'idExtended': '2420',
        'name': 'Northwestern University',
        'city': 'Evanston',
        'state': 'IL',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'northwestern.edu',
        'latitude': 42.0565,
        'longitude': -87.6753
    },
    '3508': {
        'id': 3551,
        'idExtended': '3551',
        'name': 'University of Illinois Urbana-Champaign',
        'city': 'Champaign',
        'state': 'IL',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'illinois.edu',
        'latitude': 40.1047,
        'longitude': -88.2291
    },
    # ===== NORTH CAROLINA (1) =====
    '2274': {
        'id': 943,
        'idExtended': '943',
        'name': 'Duke University',
        'city': 'Durham',
        'state': 'NC',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'duke.edu',
        'latitude': 36.0014,
        'longitude': -78.9382
    },
    # ===== MARYLAND (1) =====
    '2273': {
        'id': 1637,
        'idExtended': '1637',
        'name': 'Johns Hopkins University',
        'city': 'Baltimore',
        'state': 'MD',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'jhu.edu',
        'latitude': 39.2992,
        'longitude': -76.5934
    },
    # ===== TEXAS (3) =====
    '3696': {
        'id': 3696,
        'idExtended': '3696',
        'name': 'University of Texas at Austin',
        'city': 'Austin',
        'state': 'TX',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'utexas.edu',
        'latitude': 30.2849,
        'longitude': -97.7341
    },
    '3509': {
        'id': 2681,
        'idExtended': '2681',
        'name': 'Rice University',
        'city': 'Houston',
        'state': 'TX',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'rice.edu',
        'latitude': 29.7174,
        'longitude': -95.4018
    },
    '3510': {
        'id': 3253,
        'idExtended': '3253',
        'name': 'Texas A&M University-College Station',
        'city': 'College Station',
        'state': 'TX',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'tamu.edu',
        'latitude': 30.6187,
        'longitude': -96.3365
    },
    # ===== MICHIGAN (1) =====
    '2272': {
        'id': 3589,
        'idExtended': '3589',
        'name': 'University of Michigan-Ann Arbor',
        'city': 'Ann Arbor',
        'state': 'MI',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'umich.edu',
        'latitude': 42.2780,
        'longitude': -83.7382
    },
    # ===== TENNESSEE (1) =====
    '3511': {
        'id': 3790,
        'idExtended': '3790',
        'name': 'Vanderbilt University',
        'city': 'Nashville',
        'state': 'TN',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'vanderbilt.edu',
        'latitude': 36.1447,
        'longitude': -86.8027
    },
    # ===== INDIANA (1) =====
    '3512': {
        'id': 3634,
        'idExtended': '3634',
        'name': 'University of Notre Dame',
        'city': 'Notre Dame',
        'state': 'IN',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'nd.edu',
        'latitude': 41.7056,
        'longitude': -86.2353
    },
    # ===== RHODE ISLAND (1) =====
    '2271': {
        'id': 323,
        'idExtended': '323',
        'name': 'Brown University',
        'city': 'Providence',
        'state': 'RI',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'brown.edu',
        'latitude': 41.8268,
        'longitude': -71.4026
    },
    # ===== NEW HAMPSHIRE (1) =====
    '2270': {
        'id': 828,
        'idExtended': '828',
        'name': 'Dartmouth College',
        'city': 'Hanover',
        'state': 'NH',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'dartmouth.edu',
        'latitude': 43.7041,
        'longitude': -72.2900
    },
    # ===== MISSOURI (1) =====
    '3513': {
        'id': 3863,
        'idExtended': '3863',
        'name': 'Washington University in St. Louis',
        'city': 'St. Louis',
        'state': 'MO',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'wustl.edu',
        'latitude': 38.6488,
        'longitude': -90.3108
    },
    # ===== VIRGINIA (1) =====
    '3514': {
        'id': 3722,
        'idExtended': '3722',
        'name': 'University of Virginia-Main Campus',
        'city': 'Charlottesville',
        'state': 'VA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'virginia.edu',
        'latitude': 38.0336,
        'longitude': -78.5080
    },
    # ===== WISCONSIN (1) =====
    '3515': {
        'id': 3735,
        'idExtended': '3735',
        'name': 'University of Wisconsin-Madison',
        'city': 'Madison',
        'state': 'WI',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'wisc.edu',
        'latitude': 43.0766,
        'longitude': -89.4125
    }
}

# UTM 参数（营销追踪参数）
DEFAULT_UTM_PARAMS = {
    'utm_source': 'gemini',
    'utm_medium': 'paid_media',
    'utm_campaign': 'students_pmax_bts-slap'
}
