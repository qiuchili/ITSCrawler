import urllib3
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
from issue_tracker import IssueTracker
from patch import Patch

date_format = '%Y-%m-%dT%H:%M:%S'
http = urllib3.PoolManager()
urllib3.disable_warnings()

project = 'LUCENE'
issue_id = 8575
root_url = 'https://issues.apache.org/jira/browse/'
issue_url = os.path.join(root_url, '{}-{}'.format(project,issue_id))
response = http.request('GET', issue_url)
web_data = BeautifulSoup(response.data,features="lxml")
tracker = IssueTracker()
tracker.id = issue_id

summary_raw = web_data.title.string
summary = summary_raw.replace("- ASF JIRA","").replace("[{}-{}]".format(project,issue_id),"").strip()
tracker.summary = summary


description = web_data.find(id="description-val").get_text().strip()
tracker.description = description

for one_node in web_data.find(id = "issuedetails").find_all('div'):
	key_value_pair = one_node.get_text().split(':')
	if not len(key_value_pair) == 2:
		break
	key = key_value_pair[0].strip()
	value = key_value_pair[1].strip()
	if hasattr(tracker,key.lower()):
		setattr(tracker,key.lower(),value.lower())

create_time_str = web_data.find(id='datesmodule').find(id='created-val').time['datetime']

tracker.create_date = datetime.strptime(create_time_str[:-5], date_format)

update_time_str = web_data.find(id='datesmodule').find(id='updated-val').time['datetime']

tracker.update_date = datetime.strptime(update_time_str[:-5], date_format)

for node in web_data.find(id = 'file_attachments').find_all('div'):
	patch = Patch()
	patch.url = 'https://issues.apache.org'+node.a['href']
	patch.time = datetime.strptime(node.parent.time['datetime'][:-5],date_format)
	patch.id = int(node.parent['data-attachment-id'])
	patch_response = http.request('GET', patch.url)
	patch_data = BeautifulSoup(patch_response.data,features="lxml")
	patch.content = patch_data.get_text()
	matched_lines = [line for line in patch.content.split('\n') if "diff" in line]
	for line in matched_lines:
		strs = line.split(' ')
		file_name = strs[-1][1:]
		patch.touched_files.append(file_name)
	tracker.patch_list.append(patch)

tracker.print()
# print(tracker.patch_list)