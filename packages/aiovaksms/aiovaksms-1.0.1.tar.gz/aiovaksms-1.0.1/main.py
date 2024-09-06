from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name = 'aiovaksms',
    version='1.0.0',
    packages=find_packages(),
    long_description=description
)

# import asyncio
#
# from aiovaksms import VakSms
#
#
# async def main():
#     client = VakSms('cfb40c75fbe44c0f836af0f0a14175f0')
#
#     data = await client.set_status('1725546315697382', 'send')
#     print(data)  # Prints payment url for customer
#
#
# asyncio.run(main())

#build command: python .\main.py sdist bdist_wheel
#publish command: twine upload dist/*