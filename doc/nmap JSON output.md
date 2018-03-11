Complete JSON output
```json
nmaprun:{
	@scanner:nmap
	@args:<arg string>
	@start:<unix time>
	@startstr:<str time>
	@version:7.6
	@xmloutputversion:1.04
	verbose:{@level:0}
	debugging:{@level:0}
	runstats:{
		finished:{
			@time:<unix time>
			@timestr:<str time>
			@elapsed:<seconds>
			@summary:<str>
			@exit:<success|error>
		}
		hosts:{
			@up:<int>
			@down:<int>
			@total:<int>
		}
	}
	host:[{
		status:{
			@state:<up|down|skipped|unknown>
			@reason:<localhost-response|...>
			@reason_ttl:<int>
		}
		address:{
			@addr:<str>
			@addrtype:<ipv4|ipv6|mac>
			@vendor:<str> (only for mac)
		}
		hostnames:{
			hostname:{
				@name:<str>
				@type:<PTR|user>
			}
		}
	}]
}
```

Required JSON subset
```json
nmaprun:{
	@startstr:<str time>
	runstats:{
		finished:{
			@elapsed:<seconds>
			@summary:<str>
			@exit:<success|error>
		}
		hosts:{
			@up:<int>
			@total:<int>
		}
	}
	host:[{
		status:{
			@state:<up|down|skipped|unknown>
			@reason:<localhost-response|...>
		}
		address:[{
			@addr:<str>
			@addrtype:<ipv4|ipv6|mac>
		}]
		hostnames:{
			hostname:{
				@name:<str>
			}
		}
	}]
}
```