# Env++ Python Client
## Installation
```bash
pip install envpp
```
## Usage
First you need to register with the service:
```bash
envpp api auth sign-up
```
Then enter the email and password of the new account.
**Or if you are already registered in the service**:
```bash
envpp api auth sign-in
```
**After that, you will receive a token**. There is very little left to start using. Now let's set the token to the client:
```bash
envpp set-token {your_token_here}
```
🎉 Congratulations. Now you can add the items you need
```bash
envpp api items create --key foo --value bar
```
Generate the resulting items
```bash
envpp generate
```
Let's go back to the code
```python
# main.py
from envpp import envpp

print(envpp['foo'])
```
```bash
python main.py
> bar
```
Everything is typed
