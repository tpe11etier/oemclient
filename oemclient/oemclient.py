#!/usr/bin/env python
# coding=utf-8

import requests
import logging
import codecs
import ConfigParser
import os

from io import BytesIO
from uuid import uuid4

from requests.packages.urllib3.filepost import iter_fields
from requests.packages.urllib3.packages import six
from requests.packages.urllib3.packages.six import b



writer = codecs.lookup('utf-8')[3]

CONF = ConfigParser.ConfigParser()

try:
	CONF.read("oemclient.props")
	url = CONF.get("Oemclient", "url")
	file = CONF.get("Oemclient", "file")
	charset = CONF.get("Oemclient", "charset")
except IOError as e:
	print 'File %s not found!' % e





logging.basicConfig(filename='oemclient.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


#Embedded XML to send for submission.
XML = """
<Request errorstyle=\"separate\" version=\"EXAPI 2.0\" prunelist=\"//DeliveryBlock,//Sequence,//Block,//DeliveryRequest,//Contact\">
<domain>EA</domain>
<username>EXCHANGEtarget</username>
<password>EXCHANGEtarget</password>
<oemid>ExpressAlert</oemid>
<oempassword>12345</oempassword>
<requestType>Commit</requestType>
<Job><UserReference>775847</UserReference>
<Message>
	<subject><![CDATA[Testing Profiles API Connectivity]]></subject>
	<MessageArg>
		<Name>EMAIL_ADDR</Name>
		<Ordinal>0</Ordinal>
		<Value>support@varolii.com</Value>
	</MessageArg>
	<MessageArg>
		<Name>BODY</Name>
		<Ordinal>0</Ordinal>
		<Value>This is just a test.für</Value>
	</MessageArg>
	<MessageArg>
		<Name>PRE_THEME</Name>
		<Value>EXCHANGE:general;EXCHANGE:;VOICETALENT:DAVID;SON:M_ENG_4</Value>
	</MessageArg>
	<MessageArg>
		<Name><![CDATA[THEME]]></Name>
		<Value><![CDATA[EXCHANGE:general;EXCHANGE:;VOICETALENT:DAVID;SON:M_ENG_4;NotifyApp\EXCHANGE\EXCHANGE\general;NotifyApp\EXCHANGE\EXCHANGE;NotifyApp\EXCHANGE;NotifyApp]]></Value>
	</MessageArg>
	<MessageArg>
		<Name>SENDER</Name>
		<Value>Varolii</Value>
	</MessageArg>
</Message>
<Contact Label=\"7419868\">
	<FirstName><![CDATA[Professional]]></FirstName>
	<LastName><![CDATA[Services Admin]]></LastName>
	<Company><![CDATA[Varolii Corporation]]></Company>
	<ContactMethod Label=\"19453943\">
		<Transport>email</Transport>
		<Ordinal>0</Ordinal>
		<Qualifier>office</Qualifier>
		<EmailAddress><![CDATA[tony.pelletier@varolii.com]]></EmailAddress>
	</ContactMethod>
</Contact>
<Block>
<DeliveryRequest>
<MessagePath>Message[1]</MessagePath>
<ContactMethodPath>Contact[@Label="7419868"]/ContactMethod[@Label=\"19453943\"]</ContactMethodPath>
	<DeliveryRequestArg>
		<Name><![CDATA[USER_USERIDENTIFIER]]></Name>
		<Value><![CDATA[2181]]></Value>
		<Ordinal>0</Ordinal>
	</DeliveryRequestArg>
	<DeliveryRequestArg>
		<Name><![CDATA[Role]]></Name>
		<Value><![CDATA[Private]]></Value>
		<Ordinal>0</Ordinal>
	</DeliveryRequestArg>
</DeliveryRequest>
</Block>
</Job>
</Request>
"""

def choose_boundary():
	"""
	Our embarassingly-simple replacement for mimetools.choose_boundary.
	"""
	return uuid4().hex


def my_encode_multipart_formdata(fields, boundary=None):

	"""
Encode a dictionary of ``fields`` using the multipart/form-data mime format.

:param fields:
	Dictionary of fields or list of (key, value) field tuples.  The key is
	treated as the field name, and the value as the body of the form-data
	bytes. If the value is a tuple of two elements, then the first element
	is treated as the filename of the form-data section.

	Field names and filenames must be unicode.

:param boundary:
	If not specified, then a random boundary will be generated using
	:func:`mimetools.choose_boundary`.
"""
	body = BytesIO()
	if boundary is None:
		boundary = choose_boundary()

	for fieldname, value in iter_fields(fields):
		body.write(b('--%s\r\n' % (boundary)))

		if isinstance(value, tuple):
			filename, data = value
			#charset = 'UTF-8'
			body.write(b('Content-Type: application/x-www-form-urlencoded; charset="%s"\r\n' % charset))
			writer(body).write('Content-Disposition: form-data; name="%s"\r\n' % fieldname)
			body.write('\r\n' )

		else:
			data = value
			writer(body).write('Content-Disposition: form-data; name="%s"\r\n' % (fieldname))
			body.write(b'Content-Type: text/plain\r\n\r\n')

		if isinstance(data, int):
			data = str(data)  # Backwards compatibility

		if isinstance(data, six.text_type):
			writer(body).write(data)
		else:
			body.write(data)

		body.write(b'\r\n')

	body.write(b('--%s--\r\n' % (boundary)))

	content_type = b('multipart/form-data; boundary=%s' % boundary)

	return body.getvalue(), content_type



def event_create(url=None, file=None):
	try:
		file = open(os.path.abspath(os.path.join(os.curdir, 'xmlfiles',file)), 'rb').read()
		payload = {'PWFORM' : '38', 'PWF_MBML' : file}
		try:
			result = requests.post(url, files=payload)
			logging.debug(result.text)
			print result.text
		except Exception as e:
			print e
			print "ERROR: A connection error has occurred. "
	except IOError as e:
		print "File %s not found.  Be sure you specified a file in oemclient.props" % e



def main():
	event_create(url,file)



if __name__ == '__main__':
	main()