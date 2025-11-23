/ip firewall address-list
remove [find list=openai]
add list=openai address=104.18.32.0/24 comment="chatgpt.com"
add list=openai address=172.64.155.0/24 comment="chatgpt.com"
