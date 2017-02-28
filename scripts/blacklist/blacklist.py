# coding: utf8
import sys
import json
import urllib
import MySQLdb
import configuration 

_message = '''
----------------------------------------------------------- 예시 ------------------------------------------------------------- 
블랙리스트 조회 	: python blacklist.py r ALL ( TOP 100 ORDER BY `date-created` )
			: python blacklist.py r %EC%B5% ( Contains "%EC%B5%" ORDER BY `date-created` )
			: python blacklist.py rc stats ( COUNT(*) )
			: python blacklist.py rr 1,2,3,4,5,6 ( WHERE `id` in (1, 2, 3, 4, 5, 6) )
블랙리스트 등록 	: python blacklist.py c ew:%EC%B5%9C%EC%88%9C%EC%8B%A4
블랙리스트 삭제 	: python blacklist.py d 16
블랙리스트 status 갱신	: python blacklist.py u 16 ( 0 -> 1 / 1 -> 0 ) 
------------------------------------------------------------------------------------------------------------------------------
'''
if __name__ == '__main__': 
	
	if len(sys.argv) != 3: 
		print _message
		sys.exit(); 
	
	pycommand, mode, argument = sys.argv

	connection = MySQLdb.connect(configuration.db_host, configuration.db_user, configuration.db_password, configuration.db_name)
	connection.set_character_set('utf8')
	cursor = connection.cursor()

	result = { 'status': False, 'data': [], }  
	if mode == 'r': 
		command = 'SELECT `id`, `type`, `name`, `date-created`, `date-updated`, `status` FROM `Blacklist` %s ORDER BY `date-created` LIMIT 100' % (
			'WHERE `name` LIKE \'%%%s%%\'' % urllib.unquote(argument)
			if argument != 'ALL' else ''
		)  
		cursor.execute(command)
		for id, type, name, date_created, date_updated, status in cursor.fetchall(): 
			result['data'].append([
				id, type, name, 
				date_created.strftime('%Y-%m-%d %H:%M:%S'), 
				date_updated.strftime('%Y-%m-%d %H:%M:%S'), 
				status])
		result['status'] = len(result['data']) > 0

	elif mode == 'rc': 
		command = 'SELECT COUNT(*) FROM `Blacklist`'
		cursor.execute(command)

		for count in cursor.fetchall(): 
			result['data'] = count[0]

		result['status'] = True
	
	elif mode == 'rr': 
		command = 'SELECT `id`, `type`, `name`, `date-created`, `date-updated`, `status` FROM `Blacklist` %s ' % (
			'WHERE `id` IN (%s)' % argument
		)
		cursor.execute(command)
		for id, type, name, date_created, date_updated, status in cursor.fetchall(): 
			result['data'].append([
				id, type, name, 
				date_created.strftime('%Y-%m-%d %H:%M:%S'), 
				date_updated.strftime('%Y-%m-%d %H:%M:%S'), 
				status])
		result['status'] = len(result['data']) > 0

	elif mode == 'c': 
		type, name = argument.split(':')
		command = 'INSERT INTO `Blacklist` ( `type`, `name`, `date-created`, `date-updated` ) VALUES (%s, %s, NOW(), NOW())'
		values = [(type, urllib.unquote(name))]
		
		try: 
			cursor.executemany(command, values)
        		connection.commit()
			result['status'] = True

		except MySQLdb.IntegrityError, e: 
			pass # dulicated error 

	elif mode == 'd': 
		command = 'DELETE FROM `Blacklist` WHERE `id` = %s' 
		
		cursor.execute(command, (argument, ))
		connection.commit()
		result['status'] = True

	elif mode == 'u': 
		command = 'UPDATE `Blacklist` SET `status` = IF(`status` = 1, 0, 1) WHERE `id` = %s'
			
		cursor.execute(command, (argument, ))
		connection.commit()
		result['status'] = True

	print urllib.quote(json.dumps(result))
	
