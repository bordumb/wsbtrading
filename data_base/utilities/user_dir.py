import getpass


def user_dir():
    """ This function returns the relavant file directories and passwords for
    the current system user in a dictionary. """

    if getpass.getuser() == 'root':
        # Docker container will use these variables

        load_tables = '/load_tables'

        # PostgreSQL default database information
        main_db = 'postgres'
        main_user = 'postgres'
        main_password = 'postgres'          # Change this!!
        main_host = 'postgres_wsbtrading'          # the docker container name
        main_port = '5432'

        # PostgreSQL wsbtrading database information
        wsbtrading_db = 'wsbtrading'
        wsbtrading_user = 'postgres'
        wsbtrading_password = 'postgres'   # Change this!!
        wsbtrading_host = 'postgres_wsbtrading'   # the docker container name
        wsbtrading_port = '5432'

        # Quandl information
        quandl_token = 'xqq66bfL2zy6ijycPEWd'       # Keep this secret!!

    elif getpass.getuser() == 'briandeely':
        # Local user will use thee variables

        load_tables = '/load_tables'

        # PostgreSQL default database information
        main_db = 'postgres'
        main_user = 'postgres'
        main_password = 'postgres'          # Change this!!
        main_host = '127.0.0.1'
        main_port = '5432'

        # PostgreSQL wsbtrading database information
        wsbtrading_db = 'wsbtrading'
        wsbtrading_user = 'postgres'
        wsbtrading_password = 'postgres'   # Change this!!
        wsbtrading_host = '127.0.0.1'
        wsbtrading_port = '5432'

        # Quandl information
        quandl_token = 'xqq66bfL2zy6ijycPEWd'       # Keep this secret!!

    else:
        raise NotImplementedError('Need to set data variables for user %s in '
                                  'pySecMaster/utilities/user_dir.py' %
                                  getpass.getuser())

    return {'load_tables': load_tables,
            'postgresql':
                {'main_db': main_db,
                 'main_user': main_user,
                 'main_password': main_password,
                 'main_host': main_host,
                 'main_port': main_port,
                 'wsbtrading_db': wsbtrading_db,
                 'wsbtrading_user': wsbtrading_user,
                 'wsbtrading_password': wsbtrading_password,
                 'wsbtrading_host': wsbtrading_host,
                 'wsbtrading_port': wsbtrading_port,
                 },
            'quandl':
                {'quandl_token': quandl_token},
            }
