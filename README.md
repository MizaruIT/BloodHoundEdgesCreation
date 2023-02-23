# BloodHound Edges Creation
## 📗 Table of contents
* [📖 About the repository](#about-the-repo)
* [💻 Getting started](#getting-started)
	* [Installation](#installation)
	* [Usage](#usage)
	* [Structure of the project](#structure-project)
* [🔭 Roadmap](#roadmap)
* [👥 Contact](#contact)
* [🤝 Contributing](#contributing)


## 📖 About the repository <a name="about-the-repo"/>
A repository with different methods used for processing data during/post a penetration testing (such as via NTDS file) to create edges that could be used to compromise an Active Directory infrastructure. In brief, to ease the AD compromission.

## 💻 Getting started <a name="getting-started"/>
### Installation
To retrieve all the MIB files:
```sh 
git clone https://github.com/MizaruIT/BloodHoundEdgesCreation
cd BloodHoundEdgesCreation;
```

### Usage <a name="usage"/>
**SharesPasswordWith Edge**

If you have retrieved a NTDS file, you can parse it to create an Edge "SharesPasswordWith" between all the computers/users having the same passwords. Thus, you can visualize the users using the same passwords via BloodHound. 
```sh
# Usage
python3 bloodhoundedgescreation.py -m ntds -fp $PATH_TO_NTDS_FILE 

# RECOMMENDED CYPHER QUERIES
=> Retrieve all users with same passwords
    - MATCH p=(u:User)-[:SharesPasswordWith]->(u1:User) RETURN DISTINCT(p) 
=> Retrieve all users with the same passwords that an Admin user.
    - MATCH p=(u:User{admincount:false})-[:SharesPasswordWith]->(u1:User{admincount:true}) RETURN DISTINCT(p)
```

### Structure of the project <a name="structure-project"/>
The project has the following structure.

    ├── bloodhoundedgescreation.py         # The script used for edge creation

  ## 🔭 ROADMAP <a name="roadmap"/>
- [ ] Add others mode (some ideas, just need to add them)


## 👥 Contact <a name="contact"/>
- Twitter: @MizaruIT (https://twitter.com/MizaruIT)
- GitHub: @MizaruIT (https://github.com/MizaruIT)
- Project Link: https://github.com/MizaruIT/MIBS


## 🤝 Contributing <a name="contributing"/>
Contributions, issues, and feature requests are welcome!

Feel free to send me messages to add new MIB files.