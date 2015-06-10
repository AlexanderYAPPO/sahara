from sahara import exceptions as ex
from sahara.i18n import _
from sahara.plugins import utils as plugin_utils
from sahara.service.edp.spark import engine as edp_engine


class EdpCdhSparkEngine(edp_engine.SparkJobEngine):

    edp_base_version = "5.3.0"

    def __init__(self, cluster):
        super(EdpCdhSparkEngine, self).__init__(cluster)
        self.master = plugin_utils.get_instance(cluster, "CLOUDERA_MANAGER")
        self.plugin_params["spark-user"] = "sudo -u spark "
        self.plugin_params["spark-submit"] = "spark-submit"
        self.plugin_params["deploy-mode"] = "cluster"
        self.plugin_params["master"] = "yarn-cluster"

    @staticmethod
    def edp_supported(version):
        return version >= EdpCdhSparkEngine.edp_base_version

    def validate_job_execution(self, cluster, job, data):
        if not self.edp_supported(cluster.hadoop_version):
            raise ex.InvalidDataException(
                _('Spark {base} or higher required to run {type} jobs').format(
                    base=EdpCdhSparkEngine.edp_base_version, type=job.type))

        super(EdpCdhSparkEngine, self).validate_job_execution(cluster, job, data)