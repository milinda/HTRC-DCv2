FORMAT: 1A

# HTRC Data Capsules v2 (DCv2)

DCv2 is a API for creating and managing virtual machines for non-consumptive research on HTRC corpus.

# Group Capsules

Resources related to Data Capsules.

## Capsules Collection [/capsules]

### List All Capsules [GET]

+ Response 200 (application/json)

        [
     	    { 
     	      "id": 1,
     	      "created_at": "2014-11-11T08:40:51.620Z",
     	      "url": "/capsules/1",
     	      "host": "dchost1.htrc.indiana.edu",
     	      "mode": "M",
     	      "status": "Running",
     	      "vnc_port": 16012,
     	      "attributes": { 
     	        "memory": "1G",
     	        "vcpus": 2,
     	        "disk": "50G"
     	        "image": "ubuntu-16.04"
     	      }
     	    }, { 
     	      "id": 23,
     	      "created_at": "2015-01-23T10:50:23.340Z",
     	      "url": "/capsules/23",
     	      "host": "dchost2.htrc.indiana.edu",
     	      "mode": "S",
     	      "status": "Running",
     	      "vnc_port": 16023,
     	      "attributes": { 
     	        "ram": "2G",
     	        "vcpus": 4
     	      }
     	    }
        ]

### Create a New Capsule [POST]

Users can create data capsules using this action. It takes a JSON object containing capsules attributes such as amount of RAM and virtual CPU cores.

+ Request (application/json)

        {
          "ram": "2G",
          "vcpus": 2,
          "disk": "50G",
          "image": "ubuntu-16.04"
        }

+ Response 201 (application/json)

    + Headers
    
            Location: /capsules/25

    + Body

            { 
     	        "id": 25,
     	        "created_at": "2015-01-23T10:50:23.340Z",
     	        "url": "/capsules/25",
     	        "host": "dchost2.htrc.indiana.edu",
     	        "mode": "S",
     	        "status": "Running",
     	        "vnc_port": 16027,
     	        "attributes": { 
     	          "ram": "2G",
     	          "vcpus": 4
     	        }
     	      }

## Capsule [/capsules/{capsule_id}]

+ Parameters
    + capsule_id - ID of the Capsule in the form of an integer

### View Capsule Detail [GET]

+ Response 200 (application/json)

        { 
     	    "id": 25,
     	    "created_at": "2015-01-23T10:50:23.340Z",
     	    "url": "/capsules/25",
     	    "host": "dchost2.htrc.indiana.edu",
     	    "mode": "S",
     	    "status": "Running",
     	    "vnc_port": 16027,
     	    "attributes": { 
     	      "ram": "2G",
     	      "vcpus": 4
     	    }
     	  }

### Delete [DELETE]

+ Response 204

### Stop or Switch Mode [POST]

+ Request (application/json)

        {
          "operation": "switch_mode|stop"
        }

+ Response 200 (application/json)

         { 
     	    "id": 25,
     	    "created_at": "2015-01-23T10:50:23.340Z",
     	    "url": "/capsules/25",
     	    "host": "dchost2.htrc.indiana.edu",
     	    "mode": "S",
     	    "status": "Stopped",
     	    "vnc_port": 16027,
     	    "attributes": { 
     	      "ram": "2G",
     	      "vcpus": 4
     	    }
     	  }

# Group Images

Resources related to VM images.

# Group Disks

Resources related to VM disks.

# Group Results

Resources related to results from DC users.