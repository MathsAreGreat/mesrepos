import quopri

encoded_string = "=D9=87=D9=8A=D8=AB=D9=85=20=2E=2E=2E"

decoded_string = quopri.decodestring(encoded_string).decode("utf-8")
print(decoded_string)
