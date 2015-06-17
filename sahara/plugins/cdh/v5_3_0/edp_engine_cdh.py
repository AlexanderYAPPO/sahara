# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sahara import exceptions as ex
from sahara.i18n import _
from sahara.plugins import exceptions as pl_ex
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
                _('Cloudera {base} or higher required to run {type} jobs').format(
                    base=EdpCdhSparkEngine.edp_base_version, type=job.type))

        shs_count = plugin_utils.get_instances_count(
            cluster, 'SPARK_YARN_HISTORY_SERVER')
        if shs_count != 1:
            raise pl_ex.InvalidComponentCountException(
                'SPARK_YARN_HISTORY_SERVER', '1', shs_count)

        super(EdpCdhSparkEngine, self).validate_job_execution(cluster, job,
                                                              data)