#Hoover


A python wrapper used to hit the [Loggly](http://loggly.com "Loggly"). API 

For more information on Hoover see <http://wiki.loggly.com/hooverguide>

##Install

With this git repo:
	cd /hoover
	sudo python setup.py install
	
	

Easy Install:
	$easy_install -U hoover

Pypi: <http://pypi.python.org/pypi/Hoover>



##Using Hoover For Searching Loggly


Enter your credentials in hoover.LogglySession after importing:

	
	import hoover
	.
	.
	.
	i = hoover.LogglySession('<subdomain>','<username>','<password>')

	i.search(q='apache2 error', starttime='NOW-2DAYS', format='csv')
	i.search(q='json.priority:err', starttime='NOW-15MINUTES') #Defaults to json if format is left out

##Using Hoover For Logging to Loggly's New API

	import logging
	from hoover.handlers import LogglyHttpHandler
	.
	.
	.
	token_and_suffix = "{token}/tag/http".format(token=YOUR_LOGGLY_TOKEN_FROM_SOURCE_SETUP)
	loggly_handler = LogglyHttpHandler(token=token_and_suffix, proxy='logs-01.loggly.com')
	logger = logging.getLogger('default')
	logger.addHandler(loggly_handler)
	logger.critical("This goes straight to my Loggly!")

##Search Properties

For more details on using search within Loggly check out <http://wiki.loggly.com/searchguide>

<table>
  <tr>
    <th>Property</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>rows</td>
    <td>Number of rows returned by your query. Defaults to 10.</td>
  </tr>
  <tr>
    <td>start</td>
    <td>Offset for starting row. Defaults to 0.</td>
  </tr>
  <tr>
     <td>starttime</td>
     <td>Start time for the search.  Defaults to NOW-24HOURS.</td>
  </tr>
  <tr>
     <td>endtime</td>
     <td>End time for the search.  Defaults to NOW. </td>
  </tr>
  <tr>
     <td>order</td>
     <td>Direction of results returned, either 'asc' or 'desc'.  Defaults to 'desc'.</td>
  </tr>
  
  <tr>
     <td>callback</td>
     <td>JSONP callback to receive a JSONP response.</td>
  </tr>
   <tr>
     <td>format</td>
     <td>Output format, either 'json', 'xml', or 'text'.  Defaults to 'json'</td>
  </tr>
   <tr>
     <td>fields</td>
     <td>Which fields should be output.  One or more of the following separated by commas: 'id', 'timestamp', 'ip', 'inputname', 'text'.</td>
  </tr>
</table>

##More Functions

<table>
  
   <tr>
     <td>Function</td>
     <td>Description</td>
  </tr>
   <tr>
     <td>*.config_inputs()</td>
     <td>Configures each input in your loggly account, register a python logger
        with the input's name logging to the input.</td>
  </tr>
   <tr>
     <td>*.create_input()</td>
     <td>Creates a new input on your loggly account.</td>
  </tr>
   <tr>
     <td>*.facets()</td>
     <td>Thin wrapper on Loggly's facet search API. facetby can be input, ip, or date</td>
  </tr>
  <tr>
     <td>*.http_inputs()</td>
     <td>Lists all http inputs</td>
  </tr>
  <tr>
     <td>*.search()</td>
     <td>See above "Search Properties"</td>
  </tr>
  <tr>
     <td>*.inputs</td>
     <td>Lists all inputs</td>
  </tr>
</table>


Meta
----

Created and maintained by Mike Blume

If you have questions contact technicalsupport@solarwinds.com
