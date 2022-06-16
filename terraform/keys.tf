# Public key to use as an authorized key in the instances
# that we provision such that we can SSH into them if needed.
resource "aws_key_pair" "main" {  
  key_name   = "python-django"
  public_key = file("./keys/python-django.pub")
}
