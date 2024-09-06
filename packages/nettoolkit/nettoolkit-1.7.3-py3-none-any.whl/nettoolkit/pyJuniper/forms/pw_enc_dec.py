
# ---------------------------------------------------------------------------------------
from nettoolkit.pyNetCrypt import decrypt_type7, encrypt_type7, decrypt_file_passwords, mask_file_passwords
from nettoolkit.pyNetCrypt import juniper_decrypt, juniper_encrypt, decrypt_doller9_file_passwords, mask_doller9_file_passwords

from nettoolkit.nettoolkit.forms.formitems import *

# ---------------------------------------------------------------------------------------

def pw_enc_cisco_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		obj.event_update_element(pw_result_cisco={'value': ''})	
		_pw = encrypt_type7(i['pw_cisco'])
		obj.event_update_element(pw_result_cisco={'value': _pw})	
		return True
	except:
		return None

def pw_dec_cisco_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		obj.event_update_element(pw_result_cisco={'value': ''})	
		_pw = decrypt_type7(i['pw_cisco'])
		obj.event_update_element(pw_result_cisco={'value': _pw})	
		return True
	except:
		return None

def pw_enc_juniper_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		obj.event_update_element(pw_result_juniper={'value': ''})	
		_pw = juniper_encrypt(i['pw_juniper'])
		obj.event_update_element(pw_result_juniper={'value': _pw})	
		return True
	except:
		return None

def pw_dec_juniper_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		obj.event_update_element(pw_result_juniper={'value': ''})	
		_pw = juniper_decrypt(i['pw_juniper'])
		obj.event_update_element(pw_result_juniper={'value': _pw})	
		return True
	except:
		return None


def go_cisco_pw_decrypt_exec(obj, i):
	try:
		input_file = i['pw_file_cisco']
		output_file = input_file[:-4] + '-pw-decrypted.' + input_file[-3:]
		decrypt_file_passwords(input_file, output_file)
		return True
	except:
		return None

def go_cisco_pw_mask_exec(obj, i):
	try:
		input_file = i['pw_file_cisco']
		output_file = input_file[:-4] + '-pw-masked.' + input_file[-3:]
		mask_file_passwords(input_file, output_file)
		return True
	except:
		return None

def go_juniper_pw_decrypt_exec(obj, i):
	try:
		input_file = i['pw_file_juniper']
		output_file = input_file[:-4] + '-pw-decrypted.' + input_file[-3:]
		decrypt_doller9_file_passwords(input_file, output_file)
		return True
	except:
		return None

def go_juniper_pw_mask_exec(obj, i):
	try:
		input_file = i['pw_file_juniper']
		output_file = input_file[:-4] + '-pw-masked.' + input_file[-3:]
		mask_doller9_file_passwords(input_file, output_file)
		return True
	except:
		return None




def pw_enc_decr_frame():
	"""tab display - Password Encryptor Decryptor

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Password Encryption / Decryption utility', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Cisco Type-7', text_color="black") ],
		[sg.Text('Password string:', text_color="yellow"), 
		sg.InputText(key='pw_cisco'), 
		sg.Button("Encrypt", change_submits=True, key='go_pw_enc_cisco'),
		sg.Button("Decrypt", change_submits=True, key='go_pw_dec_cisco'),
		],
		[sg.Text('Result:',  text_color="light yellow"), 
		sg.InputText(key='pw_result_cisco', disabled=True), ],
		blank_line(),
		[sg.Text('Select Cisco Configuration file:',  text_color="yellow"), 
			sg.InputText(key='pw_file_cisco'),
			sg.FileBrowse()],
		[sg.Button("Decrypt Passwords", size=(20,1),  change_submits=True, key='go_cisco_pw_decrypt'),
		 sg.Button("Mask Passwords", size=(20,1),  change_submits=True, key='go_cisco_pw_mask')],
		under_line(80),

		[sg.Text('Juniper $9', text_color="black") ],
		[sg.Text('Password string:', text_color="yellow"), 
		sg.InputText(key='pw_juniper'), 
		sg.Button("Encrypt", change_submits=True, key='go_pw_enc_juniper'),
		sg.Button("Decrypt", change_submits=True, key='go_pw_dec_juniper'),
		],
		[sg.Text('Result:',  text_color="light yellow"), 
		sg.InputText(key='pw_result_juniper', disabled=True), ],
		blank_line(),
		[sg.Text('Select Juniper Configuration file:',  text_color="yellow"), 
			sg.InputText(key='pw_file_juniper'),
			sg.FileBrowse()],
		[sg.Button("Decrypt Passwords", size=(20,1),  change_submits=True, key='go_juniper_pw_decrypt'),
		 sg.Button("Mask Passwords", size=(20,1),  change_submits=True, key='go_juniper_pw_mask')],
		under_line(80),

		])

# ---------------------------------------------------------------------------------------
