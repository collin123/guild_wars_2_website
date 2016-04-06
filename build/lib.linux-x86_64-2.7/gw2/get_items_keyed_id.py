#!/usr/bin/env python
from rest import GuildWars2ApiV2
import json
import io

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def main():
	gw2_api = GuildWars2ApiV2()
	item_ids = gw2_api.items()
	name_dict = {}
	chunked_item_ids = []
	import pdb; pdb.set_trace()
	for group in chunker(item_ids, 100):
		items_info = gw2_api.items(group)
		for item_details in items_info:
			if not 'name' in item_details:
				continue
			name_dict[item_details['id']] = item_details['name']


	import pdb; pdb.set_trace()
	with open('organized_items_by_id.json', 'w') as f:
		json.dump(name_dict, f, sort_keys=True, indent=2, separators=(',', ': '))
	return 0

if __name__ == '__main__':
	main()
