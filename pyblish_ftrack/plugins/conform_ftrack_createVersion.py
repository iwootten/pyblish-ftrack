import pyblish.api
import ftrack

@pyblish.api.log
class FtrackCreateVersion(pyblish.api.Conformer):
    """ Creates ftrack version for currently running publish.

        Arguments:
            ftrackData (dictionary): Necessary ftrack information gathered by select_ftrack
            ftrackComponents (list): list of dictionaries describing components
                item (dict): required keys in dictionary:
                    name (string): name of the component
                    path (string): path of the component
            createFtrackVersion (boolean): boolean variable set by validate_ftrack_version
    """

    order = pyblish.api.Conformer.order + 0.1
    families = ['*']
    hosts = ['*']
    version = (0, 1, 0)
    optional = True

    def process_instance(self, instance):


        if instance.has_data('ftrackComponents'):
            if instance.context.data('createFtrackVersion'):
                self.log.debug('CREATING VERSION')
                version_number = instance.context.data('version')
                ftrack_data = instance.context.data('ftrackData')
                taskid = ftrack_data['Task']['id']

                asset = ftrack.Asset(id=ftrack_data['Asset']['id'])
                self.log.debug('Using ftrack asset {}'.format(asset.getName()))

                version = asset.createVersion(comment='', taskid=taskid)

                if int(version.getVersion()) != version_number:
                    version.set('version', value=version_number)

                ftrack_data['AssetVersion'] = {'id': version.getId(),
                                               'number': version_number,
                                               }
                version.publish()
        else:
            msg = "Didn't create ftrack version."
            msg += " ftrackComponents argument not found."
            self.log.warning(msg)
