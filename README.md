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
To install the project
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
-   [ ] Parsing CME shares, and add the list of shares (ex: SMB $IP $PORT $WORKSTATION_NAME [+] ... //IP/SHARE) to an attribute shares (+ add/update the rights depending on the user used) | command : cme smb $RANGE --shares
-   [ ] Parsing CME SMB Signing value (same as above) | command : cme smb $RANGE
-   [ ] Parsing CME pwd policies (same as above) | command : cme smb $RANGE -u '$USER' -p '$PWD' --pass-pol
-   [ ] Parsing results from my scanners / or from cme mode (command : cme smb $IP -u '' -p '' -M zerologon|petitpotam|nopac)
- [x] Take into account domain name, and not only username when parsing NT + LM


## 👥 Contact <a name="contact"/>
- Twitter: @MizaruIT (https://twitter.com/MizaruIT)
- GitHub: @MizaruIT (https://github.com/MizaruIT)
- Project Link: https://github.com/MizaruIT/BloodHoundEdgesCreation


## 🤝 Contributing <a name="contributing"/>
Contributions, issues, and feature requests are welcome!

Feel free to send me messages to add new BloodHound Edges.
