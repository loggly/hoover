#Hoover


A python wrapper used to hit the Loggly API

For more information on Hoover see <http://wiki.loggly.com/hooverguide>

##Install

With this git repo:
	cd /hoover
	sudo python setup.py install
	
	

Easy Install:
	$easy_install -U hoover

Pypi:

<http://pypi.python.org/pypi/Hoover>



##Using Hoover


Enter your credentials in hoover.LogglySession after importing:

	
	import hoover
	.
	.
	.
	i = hoover.LogglySession('<subdomain>','<username>','<password>')

	i.search(q='apache2 error', starttime='NOW-2DAYS', format='csv')
	i.search(q='json.priority:err', starttime='NOW-15MINUTES') #Defaults to json if format is left out


##Search Properties


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
     <td><Start time for the search.  Defaults to NOW-24HOURS.</td>
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

##Search Guide


Be Aware:

* Does not support case-sensitive searches. Everything is case-insensitive.
* Punctuations are not search-able. For example, '[' or ']' are not indexed, so a search for: '[error]' is the same as a search for 'error'
* Right now, we break on case-changes or changes from numerical to alpha characters. So, a search for 'www' will find results containing 'www111' or 'www112ww'.


##More Functions

<table>
  
   <tr>
     <td>Function</td>
     <td>Description</td>
  </tr>
   <tr>
     <td>*.config_inputs()</td>
     <td></td>
  </tr>
   <tr>
     <td>*.create_input()</td>
     <td></td>
  </tr>
   <tr>
     <td>*.facets()</td>
     <td></td>
  </tr>
  <tr>
     <td>*.http_inputs()</td>
     <td></td>
  </tr>
  <tr>
     <td>*.search()</td>
     <td></td>
  </tr>
</table>


Meta
----

Created and maintained by Mike Blume

If you have questions contact support@loggly.com
