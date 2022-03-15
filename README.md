# MPK API
![GitHub last commit](https://img.shields.io/github/languages/count/rostekus/MPK-API) ![GitHub last commit](https://img.shields.io/apm/l/vim-mode)
![GitHub last commit](https://img.shields.io/tokei/lines/github/rostekus/MPK-API) ![GitHub last commit](https://img.shields.io/github/last-commit/rostekus/MPK-API)
![MPK_API_🚌](https://user-images.githubusercontent.com/34031791/155426157-4108fb34-3576-4f27-ba6f-c153ff8b4f7f.png)


> MPK LODZ API for Amazon AWS Cloud.
> 

---

### Table of Contents

- [Description](#description)
- [Project Organization](#project-organization)
- [How To Use](#how-to-use)
- [License](#license)
- [Author Info](#author-info)

---

## Description

Creating ReadMe's for your Github repository can be tedious.  I hope this template can save you time and effort as well as provide you with some consistency across your projects.
#### Project Organization
Project Organization
------------

    ├── README.md           <- README for developers using this project.
    ├── data                <- Json files for uploading to AWS S3
    ├── src                 <- Source files
    │   ├── aws             <- AWS lambda fucntions 
    │   ├── kdtree          <- Module for creating KDtree
    │   ├── stops           <- Module for obtaining location of stops
    │   └── timetable       <- Module for parsing data MPK Lodz page
    ├── tests               <- Pytests
    
---
## How To Use

#### Installation
Clone the repository
```
git clone https://github.com/rostekus/MPK-API
```
Setup up
```
cd MPK-API
python3 setup.py install
```
If you want to create your own database,
Specify your Google API KEY in stop.py and run
```
python3 src/run.py
```
If you want to deploy MPK API on AWS follow tutorial:
[youtube](https://www.youtube.com/watch?v=M91vXdjve7A)
You should also create S3 bucked named mpkapi

---
    
#### Technologies

- Python3
- AWS
- BS4

## License

MIT License

Copyright (c) [2021] [Rostyslav Mosorov]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Author Info

- E-mail - [rmosorov@icloud.com](rmosorov@icloud.com)


[Back To The Top](#read-me-template)
