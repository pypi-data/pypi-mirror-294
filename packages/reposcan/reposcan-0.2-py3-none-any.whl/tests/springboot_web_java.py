import re
from helpers.Helper import Helper

text = """
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/tag")
public class MyController {

    @GetMapping("/test1/{pathParameter1}")
    @RequestMapping(value = "/{pathParameter1}/page-{pathParameter2}", method = {RequestMethod.GET, RequestMethod.POST})
    @RequestMapping(value = "/{pathParameter1}/page-{pathParameter2}/xyz", method = RequestMethod.GET)
    public ResponseEntity<Object> test1(
        @PathVariable String pathParameter1,
        @PathVariable(required = false) Integer pathParameter2,
        @RequestParam(required = false) String queryParameter1,
        @RequestParam(required = false) String queryParameter2,
        @RequestHeader HttpHeaders headers,
        @RequestBody(required = false) YourRequestBodyClass bodyParameters,
        @RequestHeader("Content-Type") String contentType
    ) {
        HttpHeaders responseHeaders = new HttpHeaders();
        responseHeaders.setContentType(MediaType.valueOf(contentType));

        if ("application/xml".equals(contentType)) {
            return new ResponseEntity<>("<response><message>XML format</message></response>", responseHeaders, HttpStatus.UNSUPPORTED_MEDIA_TYPE);
        } else {
            return new ResponseEntity<>(Collections.singletonMap("incomes", incomes), responseHeaders, HttpStatus.OK); // Replace `incomes` with your data
        }
    }

    @GetMapping("/test2")
    public ResponseEntity<Void> test2() {
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
"""
text2 = """
package com.virtualpairprogrammers.api.services;

import java.util.Collection;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.virtualpairprogrammers.api.domain.VehiclePosition;

@FeignClient(url="${position-tracker-url}", name="fleetman-position-tracker")
public interface RemotePositionMicroserviceCalls 
{
	@RequestMapping(method=RequestMethod.GET, value="/vehicles/")
	public Collection<VehiclePosition> getAllLatestPositions();
	
	@RequestMapping(method=RequestMethod.GET, value="/history/{vehicleName}")
	public Collection<VehiclePosition> getHistoryFor(@PathVariable("vehicleName") String vehicleName);

	@RequestMapping(method=RequestMethod.GET, value="/vehicles/{vehicleName}")
	public VehiclePosition getLastReportFor(@PathVariable("vehicleName") String vehicleName);
}

package com.virtualpairprogrammers.api.services;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@FeignClient(url="${staff-service-url}", name="fleetman-staff-service")
public interface RemoteStaffMicroserviceCalls 
{
	@RequestMapping(method=RequestMethod.GET, value="/driver/{vehicleName}", produces = "application/json")
	public String getDriverFor(@PathVariable("vehicleName") String vehicleName);
}

"""
text3 = """
package com.virtualpairprogrammers.photos.rest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.virtualpairprogrammers.photos.services.PhotoService;

@RestController
public class PhotosController {

	@Autowired
	private PhotoService photoService;

	@RequestMapping(method=RequestMethod.GET, value="/photo/{driverName}", produces="application/json")
	public String getPhotoFor(@PathVariable String driverName)
	{
		return photoService.getPhotoFor(driverName);
	}
	
}

"""
text3 = """
package com.virtualpairprogrammers.staffmanagement.rest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.virtualpairprogrammers.staffmanagement.domain.StaffRecord;
import com.virtualpairprogrammers.staffmanagement.services.ExternalDriverMonitoringSystem;
import com.virtualpairprogrammers.staffmanagement.services.StaffService;

@RestController
public class StaffManagementController {

	@Autowired
	private StaffService staffService;
	
	@Autowired
	private ExternalDriverMonitoringSystem externalDriverMonitoringSystem;

	@RequestMapping(method=RequestMethod.GET, value="/driver/{vehicleName}", produces="application/json")
	public StaffRecord getDriverAssignedTo(@PathVariable String vehicleName)
	{
		return staffService.getDriverDetailsFor(vehicleName);
	}
	
	// See case #22 for details of this odd design...
	@RequestMapping(method=RequestMethod.POST, value="/driver/{vehicleName}/{speed}")
	public void updateSpeedLogFor(@PathVariable String vehicleName, @PathVariable String speed)
	{
		StaffRecord driverDetails = this.getDriverAssignedTo(vehicleName);
		externalDriverMonitoringSystem.updateSpeedLogFor(driverDetails.getName(), speed);
	}
	
	
}

"""
text4 = """
package com.virtualpairprogrammers.tracker.rest;

import java.text.ParseException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.virtualpairprogrammers.tracker.data.Data;
import com.virtualpairprogrammers.tracker.domain.VehiclePosition;

@RestController
public class IncomingReportsController {
	
	@Autowired
	private Data data;
		
	@RequestMapping( method=RequestMethod.POST, value="/vehicles/")
	public void receiveUpdatedPostion(@RequestBody VehiclePosition newReport) throws ParseException 
	{
		data.updatePosition(newReport);
	}

	@RequestMapping(method=RequestMethod.DELETE, value="/vehicles/")
	public void resetHistories()
	{
		data.reset();
	}
}

package com.virtualpairprogrammers.tracker.rest;

import java.util.Collection;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.virtualpairprogrammers.tracker.data.Data;
import com.virtualpairprogrammers.tracker.domain.VehicleNotFoundException;
import com.virtualpairprogrammers.tracker.domain.VehiclePosition;

@RestController
public class PositionReportsController 
{
	@Autowired
	private Data data;

	@RequestMapping(method=RequestMethod.GET,value="/vehicles/{vehicleName}")
	public VehiclePosition getLatestReportForVehicle(@PathVariable String vehicleName) throws VehicleNotFoundException
	{
		VehiclePosition position = data.getLatestPositionFor(vehicleName);
		return position;
	}

	@RequestMapping(method=RequestMethod.GET, value="/history/{vehicleName}")
	public Collection<VehiclePosition> getEntireHistoryForVehicle(@PathVariable String vehicleName) throws VehicleNotFoundException
	{
		return this.data.getHistoryFor(vehicleName);
	}

	@RequestMapping(method=RequestMethod.GET, value="/vehicles/")
	public Collection<VehiclePosition> getUpdatedPositions(@RequestHeader Map<String, String> headers)
	{
		System.out.println("Position tracker called - here's all the headers....");
		
	    headers.forEach((key, value) -> {
	        System.out.println(String.format("Header '%s' = %s", key, value));
	    });

		Collection<VehiclePosition> results = data.getLatestPositionsOfAllVehicles();
		return results;
	}
}
package com.virtualpairprogrammers.tracker.externalservices;

import java.math.BigDecimal;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.virtualpairprogrammers.tracker.domain.VehiclePosition;

@FeignClient(url="${telemetry-url}", name="fleetman-vehicle-telemetry")
public interface TelemetryRestService 
{
	@RequestMapping(method=RequestMethod.POST, value="/vehicles/")
	public void updateData(VehiclePosition data);

	@RequestMapping(method=RequestMethod.GET, value="/vehicles/{vehicleName}")
	public BigDecimal getSpeedFor(@PathVariable("vehicleName") String vehicleName);
}
package com.virtualpairprogrammers.tracker.externalservices;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@FeignClient(name="staffService", url="${staff-service-url}")
public interface DriverMonitoringService {
	@RequestMapping(method=RequestMethod.POST, value="/driver/{vehicleName}/{speed}")
	public void updateSpeedDataFor(@PathVariable("vehicleName") String vehicleName, @PathVariable("speed") String speed); 
}

"""
text5 = """
package com.virtualpairprogrammers.telemetry.rest;

import java.math.BigDecimal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.virtualpairprogrammers.telemetry.service.VehiclePosition;
import com.virtualpairprogrammers.telemetry.service.VehicleTelemetryService;

@RestController
public class VehicleTelemetryRestController 
{
	@Autowired
	private VehicleTelemetryService service;
	
	@RequestMapping(method={RequestMethod.POST, RequestMethod.GET, RequestMethod.DELETE}, value="/vehicles/")
	public void updateData(@RequestBody VehiclePosition data)
	{
		this.service.updateData(data);
	}
	@RequestMapping(method=RequestMethod.GET, value="/vehicles/{vehicleName}")
	public BigDecimal getSpeedFor(@PathVariable("vehicleName") String vehicleName)
	{
		return this.service.getSpeedFor(vehicleName);
	}
}
"""

apiPattern = r'''((?:(?:@RequestMapping|@GetMapping|@PostMapping)\(.*(?:value = )?\"(?P<paths>.*)\".*\n)|(?:@RequestMapping.*?\{?(.*(RequestMethod\.(?P<httpMethods1>\w+) ?)*?)\}?.*\n)|(?:@(?P<httpMethods2>.*)Mapping\(.*\n)|(?:@RequestMapping.*?\(.*?((?:consumes|produces) = (?P<contentTypes>\{[^}]+\}).*)\n)|(?:(?:public|protected|private) \S+ (?P<functionName>\w+)\(.*\n)|(?:@PathVariable.* (?P<pathParameters>\S+),.*\n)|(?:.*@RequestParam.* (?P<queryParameters>\S+),.*\n)|(?:@RequestHeader.* (?P<headerParameters>\S+),.*\n)|(?:@RequestBody.* (?P<bodyParameters>\S+),.*\n)|(?:return ResponseEntity.(?P<responseCodes>\w+).*\n)|.*?\n)*?(?:(?:(?P<firstSeparatorPart>.*\n\n)(?P<secondSeparatorPart>.*@))|\Z)'''

# Loop all api matches
apiMatches = re.finditer(apiPattern, text)
apiMatches = [apiMatch for apiMatch in apiMatches if apiMatch.group(0).strip() != ""]
linePatterns = Helper.getLinePatterns(apiPattern)
secondSeparatorParts= [""]
for apiMatch in apiMatches:
    apiMatchResult = Helper.getAPIMatchResult(apiMatch, linePatterns, secondSeparatorParts)
    if apiMatchResult and ("paths" in apiMatchResult or "httpMethods" in apiMatchResult):
        print(apiMatchResult)
