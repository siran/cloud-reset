# Cloud-Reset

Deletes resources from a Cloud provider account.
Resources to be deleted are specified in a YAML file, like

```
- aws_ec2:
- aws_s3:
    exclude:
        - Name: /-terraform-/ # regular expression
        - Name: /-xxx-/
    options:
        force: true           # deletes bucket contents
- aws_kms:
```

## Getting Started

Clone the repo
```
git clone git@github.com:siran/cloud-reset.git
```

### Prerequisites

Install dependencies (virtual environment recommended)
```
pip3 install -r requirements.txt
```

### Installing

After cloning the repo and installing dependencies there is nothing else to do.


## Running the tests

No tests yet.


## Built With

* Boto3

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Shashi
* Thanks to Annalect for giving me the need to develop this tool

