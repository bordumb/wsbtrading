import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from utilities.user_dir import user_dir

__author__ = 'bordumb'
__copyright__ = 'Copyright (C) 2018 Josh Schertz'
__description__ = 'An automated system to store and maintain financial data.'
__email__ = 'bordumb[AT]gmail[DOT]com'
__license__ = 'GNU AGPLv3'
__maintainer__ = 'bordumb'
__status__ = 'Development'
__url__ = 'https://bordumb.com/'
__version__ = '1.5.0'

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


def create_database(admin_user='postgres', admin_password='postgres',
                    database='wsbtrading', user='postgres'):
    """ Determine if the provided database exists within the postgres server.
    If the database doesn't exist, create it using the provided user as the
    owner. This requires connecting to the default database before psycopg2 is
    able to send an execute command.

    NOTE: The provided user must have a valid login role within postgres before
    they are able to log into the server and create databases.

    :param admin_user: String of the database admin user
    :param admin_password: String of the database admin password
    :param database: String of the database to create
    :param user: String of the user who should own the database
    """

    userdir = user_dir()['postgresql']

    conn = psycopg2.connect(database=userdir['main_db'],
                            user=admin_user,
                            password=admin_password,
                            host=userdir['main_host'],
                            port=userdir['main_port'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        with conn:
            cur = conn.cursor()

            cur.execute("""SELECT datname FROM pg_catalog.pg_database
                        WHERE lower(datname)=lower('%s')""" % database)
            database_exist = cur.fetchone()

            if not database_exist:
                cur.execute("""CREATE DATABASE %s OWNER %s""" %
                            (database, user))
            else:
                print('The %s database already exists.' % database)

            cur.close()

    except psycopg2.Error as e:
        conn.rollback()
        print('Failed to create the %s database' % database)
        print(e)
        return
    except conn.OperationalError:
        print('Unable to connect to the SQL Database in create_database. Make '
              'sure the database address/name are correct.')
        return
    except Exception as e:
        print(e)
        raise SystemError('Error: An unknown issue occurred in create_database')


def data_tables(database='wsbtrading', user='postgres',
                password='postgres', host='localhost', port=5432):

    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)

    try:
        with conn:
            cur = conn.cursor()

            def fundamentals_daily(c):
                c.execute("""
                    CREATE TABLE IF NOT EXISTS fundamentals_daily
                    (
                        ticker	    TEXT,
                        date	    TIMESTAMP WITH TIME ZONE    NOT NULL,
                        lastupdated	TIMESTAMP WITH TIME ZONE,
                        ev	        TEXT,
                        evebit	    TEXT,
                        evebitda    TEXT,
                        marketcap	TEXT,
                        pbook	    TEXT,
                        pearnings   TEXT,
                        psales      TEXT
                    )
                """)
                # This is ideal, but breaks on import ERROR: COPY fundamentals_daily, line 2, column ps: ""
                # c.execute("""
                #     CREATE TABLE IF NOT EXISTS fundamentals_daily
                #     (
                #         ticker	    TEXT,
                #         date	    TIMESTAMP WITH TIME ZONE    NOT NULL,
                #         lastupdated	TIMESTAMP WITH TIME ZONE,
                #         ev	        DECIMAL(40,4),
                #         evebit	    DECIMAL(40,4),
                #         evebitda    DECIMAL(40,4),
                #         marketcap	DECIMAL(40,4),
                #         pbook	    DECIMAL(40,4),
                #         pearnings   DECIMAL(40,4),
                #         psales      DECIMAL(40,4)
                #     )
                # """)

            def share_prices_daily(c):
                c.execute("""
                    CREATE TABLE IF NOT EXISTS share_prices_daily
                    (
                        ticker	    TEXT,
                        date	    TIMESTAMP WITH TIME ZONE    NOT NULL,
                        open	    DECIMAL(40,4),
                        high	    DECIMAL(40,4),
                        low         DECIMAL(40,4),
                        close	    DECIMAL(40,4),
                        volume	    DECIMAL(40,4),
                        dividends	DECIMAL(40,4),
                        closeunadj  DECIMAL(40,4),
                        lastupdated	TIMESTAMP WITH TIME ZONE
                    )
                """)


            def stock_tickers(c):
                c.execute("""
                    CREATE TABLE IF NOT EXISTS stock_tickers
                    (
                        table_nickname	    TEXT,
                        permaticker         INTEGER,
                        ticker	            TEXT,
                        company_name	    TEXT,
                        exchange	        TEXT,
                        isdelisted	        TEXT,
                        category	        TEXT,
                        cusips	            TEXT,
                        siccode	            TEXT,
                        sicsector	        TEXT,
                        sicindustry	        TEXT,
                        famasector	        TEXT,
                        famaindustry	    TEXT,
                        sector	            TEXT,
                        industry	        TEXT,
                        scalemarketcap	    TEXT,
                        scalerevenue	    TEXT,
                        relatedtickers	    TEXT,
                        currency	        TEXT,
                        location	        TEXT,
                        lastupdated	        TEXT,
                        firstadded	        TEXT,
                        firstpricedate	    DATE,
                        lastpricedate	    DATE,
                        firstquarter	    DATE,
                        lastquarter	        DATE,
                        secfilings	        TEXT,
                        companysite         TEXT
                    )
                """)

            fundamentals_daily(cur)
            share_prices_daily(cur)
            stock_tickers(cur)

            conn.commit()
            cur.close()

            print('All tables in data_tables are created')

    except psycopg2.Error as e:
        conn.rollback()
        print('Failed to create the data tables in the database')
        print(e)
        return
    except conn.OperationalError:
        print('Unable to connect to the SQL Database in data_tables. Make '
              'sure the database address/name are correct.')
        return
    except Exception as e:
        print(e)
        raise SystemError('Error: An unknown issue occurred in data_tables')


if __name__ == '__main__':

    create_database()
    data_tables()
