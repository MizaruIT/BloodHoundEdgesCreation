import argparse
from neo4j import GraphDatabase

class ModesEdgeCreation:
    def __init__(self, mode):
        self.mode = mode
    #############################################
    # MODE = Edge : SharesPasswordWith          #
    #############################################
    def parse_ntds(self, filename):
        all_results = []
        for line in filename:
            if ":::" not in line or '$' in line: 
                continue
            line = line.replace("\r", "").replace("\n", "")
            if (line == ""):
                continue
            else:
                line = line.split(":")
            to_append = []
            if (line[0].split("\\")[0] == line[0]):
                # no domain found, local account
                to_append.append(line[0])
                to_append.append("")
            else:
                to_append.append(line[0].split("\\")[1])
                to_append.append(line[0].split("\\")[0])
            to_append.append(line[1])
            to_append.append(line[2])
            to_append.append(line[3])
            all_results.append(to_append)
        return all_results

    #####################################################
    ################## VIA CRACKMAPEXEC #################

    ##################################################
    # MODE = Attributes : smbSigning (false or true) #
    ##################################################
    # def parse_cme_smbsigning(self, filename):
    #     all_results = []
    #     for line in filename:
    #         if "smbsigning=True" in line:
    #             smbsigning=True
    #         elif "smbsigning=False" in line:
    #             smbsigning=False
    #         workstation_name = line.split("\(smbsigning")[1]
    #         workstation_name = workstation_name.split(":")[1].split("\)")[0]
    #         all_results.append([workstation_name, smbsigning])
    #     return all_results
    
    # def parse_cme_shares(self, filename):



class ImportDataBloodHound:
    def __init__(self, uri, user, password, domain):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.domain = domain

    def set_ntlmhash(self, list_results):
        for user in list_results:
            query = f"MATCH (u:User) WHERE toUpper(u.name) CONTAINS '{user[0].upper()}@' AND toUpper(u.domain) CONTAINS '{self.domain.upper()}' SET u.LM = '{user[3]}', u.NT ='{user[4]}'"
            with self.driver.session() as session:
                with session.begin_transaction() as tx:
                    result = tx.run(query)

    def create_sharespassword_edge(self):
        query = "MATCH (u:User) WHERE u.NT IS NOT NULL OR u.LM IS NOT NULL MATCH (u1:User) WHERE u1.NT=u.NT AND u1.name<>u.name MERGE (u1)-[:SharesPasswordWith]-(u)"
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                result = tx.run(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BloodHound Edges creation")
    parser.add_argument('-b', '--bolt', type=str, default="bolt://localhost:7687", help="Connection to Bolt Neo4j database (ex: bolt://localhost:7687)")
    parser.add_argument('-u', '--username', type=str, default="neo4j", help="Neo4j username (ex : neo4j)")
    parser.add_argument('-p', '--password', type=str, default="exegol4thewin", help="Neo4j password (ex : password)")
    parser.add_argument('-d', '--domain', type=str, help="Active Directory Domain of the file (ex: NTDS dumped from X=domain)")
    parser.add_argument("-M", "--mode", choices=["ntds"], required=True, type=str.lower, default="ntds", help="Mode")
    parser.add_argument("-fp","--filepath", help="Path to the NTDS file (ex: /home/test/ntds2022)",type=str)
    args = parser.parse_args()
    mode_creation = ModesEdgeCreation(args.mode)
    if args.mode == "ntds":
        if not args.filepath or not args.domain:
            print("You don't have specified the path to the NTDS file (-fp) or the domain targeted (-d)...")
        else:
            importdata = ImportDataBloodHound(args.bolt, args.username, args.password, args.domain) # put your creds for Neo4j + the URL
            file_ntds = open(args.filepath, encoding="utf-8")
            fileresults = mode_creation.parse_ntds(file_ntds)
            importdata.set_ntlmhash(fileresults)
            importdata.create_sharespassword_edge()
            # queries in bloodhound to look at the graph where user shares password : 
            # - MATCH p=(u:User)-[:SharesPasswordWith]->(u1:User) RETURN DISTINCT(p)
            # - MATCH p=(u:User{path_candidate:true})-[:SharesPasswordWith]->(u1:User{is_da:true}) RETURN DISTINCT(p)