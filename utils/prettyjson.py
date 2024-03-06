from typing import List, Dict


def unpack(type_infos: List[Dict]) -> List[Dict]:
    clean_json = []

    for type_info in type_infos:
        clean_json.append(type_info['info'])

    return clean_json
