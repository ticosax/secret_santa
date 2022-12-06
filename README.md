# Secret Santa for your familly and friends organization

## create config file

```toml
# participants.toml
title = 'Groups To Make'

[participants]

[participants.alice]
exclusions = ['bob']

[participants.bob]
exclusions = ['alice']

[participants.kevin]
exclusions = []

[participants.jessica]
exclusions = []
```

## invoke
```sh
santa participants.toml
```

Should output something like
```
alice should give to kevin
bob should give to jessica
kevin should give to bob
jessica should give to alice
```
