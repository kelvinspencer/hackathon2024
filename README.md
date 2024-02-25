# hackathon2024

### Source:
  - https://fastapi.tiangolo.com/deployment/docker/


## How to Add a Doc
- Method: POST
- http://localhost/add_doc
```
{
	"documents": [
		"Document Name 1",
		"Document Name 2"
	],
	"metadatas": [
		"{\"source\":\"source-tag\",\"tag\":\"custom-tag\"}",
		"{\"source\":\"other-tag\"}"
	],
	"ids": [
		"1",
		"2"
	]
}
```


## How to Search a Doc by String
### Method 1
- Method: POST
- http://localhost/docs/query
```
{
	"query": "Windows"
}
```

### Method 2
- Method: GET
- http://localhost/find_by_str/Windows


## How to Empty Database (For Testing Purposes)
- Method: GET 
- http://localhost/delete_all_docs


