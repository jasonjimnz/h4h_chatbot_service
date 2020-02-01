from neo4j import GraphDatabase, basic_auth


class GraphInstance(object):
    driver = None
    session = None
    queries = {
        'ADD_MESSAGE': """
        MERGE (u:User {{ user_id: {user_id} }})
        MERGE (m:Message {{text: "{message}" }} )
        MERGE (rd: RawData {{ type: "{data_type}", name: "{name}", value: "{value}" }} )
        MERGE (u)->[r:SENDS]->(m)-[r1:CONTAINS]->(rd)->[r2:RELATED_TO]->(u)
        RETURN u,m,rd LIMIT 10
        """
    }

    def __init__(self, host, port, user, password):
        self.driver = GraphDatabase.driver(
            'bolt://{host}:{port}'.format(
                host=host,
                port=port
            ),
            auth=basic_auth(
                user=user,
                password=password
            )
        )
        self.session = self.create_session(self.driver)

    @classmethod
    def create_session(cls, driver):
        return driver.session()

    def run_query(self, session, query, debug=False):
        if debug:
            print(query)
        return session.run(query)
