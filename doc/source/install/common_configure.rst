2. Edit the ``/etc/senlin_tempest_plugin/senlin_tempest_plugin.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://senlin_tempest_plugin:SENLIN_TEMPEST_PLUGIN_DBPASS@controller/senlin_tempest_plugin
