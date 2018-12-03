class IssueTracker(object):

	def __init__(self):
		self.id = None
		self.summary = None
		self.description = None
		self.type = None
		self.status = None
		self.priority = None
		self.owner = None
		self.creater = None
		self.is_private = False
		self.crate_date = None
		self.update_date = None
		self.patch_list = []

	def print(self):
		print('issue id: {}'.format(self.id))
		print('summary: {}'.format(self.summary))
		print('description: {}'.format(self.description))
		print('type: {}'.format(self.type))
		print('priority: {}'.format(self.priority))
		print('owner: {}'.format(self.owner))
		print('creater: {}'.format(self.creater))
		print('is_private: {}'.format(self.is_private))
		print('create_date: {}'.format(self.create_date))
		print('update_date: {}'.format(self.update_date))
		print('************************')
		print('patch_list: ')
		for patch in self.patch_list:
			print('patch_id: {}'.format(patch.id))
			print('touched_files:')
			for file in patch.touched_files:
				print(file)
			print('***********************')
	# def set_id(self, issue_id):
	# 	self.id = issue_id

	# def set_summary(self, summary):
	# 	self.summary = summary

	# def set_description(self, description):
	# 	self.description = description

	# def set_status(self, status):
	# 	self.status = status

	# def set_owner(self, owner):
	# 	self.owner = owner

	# def get_owner(self):
	# 	return self.owner

	# def set_owner(self, owner):
	# 	self.owner = owner

	# def get_owner(self):
	# 	return self.owner

	# def set_owner(self, owner):
	# 	self.owner = owner

	# def get_owner(self):
	# 	return self.owner
