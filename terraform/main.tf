terraform {
  required_version = ">= 0.12"

  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "geekzone"

    workspaces {
      name = "cicd-ec2"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}


module "networking" {
  source = "./networking"
  cidr   = "10.0.0.0/16"

  az-subnet-mapping = [
    {
      name = "subnet1"
      az   = "eu-west-2a"
      cidr = "10.0.0.0/24"
    },
    {
      name = "subnet2"
      az   = "eu-west-2c"
      cidr = "10.0.1.0/24"
    },
  ]
}

# Create a security group 
resource "aws_security_group" "allow-ssh-and-egress" {
  name = "main"

  description = "Allows SSH traffic into instances as well as all eggress."
  vpc_id      = module.networking.vpc-id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh-all"
  }
}



/*
  provision an ec32 instance and will need to  trigger the circleci
*/
resource "aws_instance" "inst1" {
  instance_type = "t2.micro"
  ami           = data.aws_ami.ubuntu.id
  key_name      = "aws_key"
  subnet_id     = module.networking.az-subnet-id-mapping["subnet1"]
  user_data     = file("./deploy/templates/user-data.sh")

  vpc_security_group_ids = [
    "${aws_security_group.allow-ssh-and-egress.id}",
  ]
  provisioner "file" {
    source      = "./deploy/templates/ec2-caller.sh"
    destination = "/home/ubuntu/ec2-caller.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/ubuntu/ec2-caller.sh",      
    ]
  }

  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ubuntu"
    private_key = file("./keys/aws_key_enc")
    timeout     = "4m"
  }
}
