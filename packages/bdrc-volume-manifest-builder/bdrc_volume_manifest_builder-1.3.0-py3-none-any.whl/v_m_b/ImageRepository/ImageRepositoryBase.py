"""
Base class for image repositories
"""

from abc import ABCMeta, abstractmethod
import logging

import v_m_b.manifestCommons as Common


class ImageRepositoryBase(metaclass=ABCMeta):


    @abstractmethod
    def manifest_exists(self, work_Rid: str, image_group_name: str) -> bool:
        """
        Test if a manifest exists
        :param work_Rid: work identifier
        :param image_group_name: which image group (volume)
        :return: true if the args point to a path containing a 'dimensions.json' object
        """
    @abstractmethod
    def resolve_work(self, work_rid: str) -> (object, str):
        """
        Resolve a work RID to a path and identifier
        :param work_rid: work identifier
        :return: path to the work
        """
        pass

    pass


    @abstractmethod
    def generateManifest(self, work_Rid: str, vol_infos: str) -> []:
        """
        Generates the manifest for one image group. The manifest contains entries for each image.
        See manifestCommons.fillBlobDataWithImage
        :param work_Rid: Work name
        :type work_Rid: str
        :param vol_infos: data structure of volumes
        :type vol_infos: VolInfo
        :return: manifest as list of dictionaries
        """
        pass

    @abstractmethod
    def uploadManifest(self, work_rid: str, image_group: str, bom_name: str,  manifest_zip: bytes):
        """
        Uploads a zip string of a manifest object
        :param work_rid: locator
        :param image_group: locator
        :param bom_name: filename of target
        :param manifest_zip: payload
        :type manifest_zip: bytes
        :return:
        """


    def clean_manifest(self, manifest: [dict]):
        """
        :param manifest: file list
        :return: reduced set, only files without errors
        """
        self.repo_log.info(f"cleaning manifest removed: {[x for x in manifest if 'error'  in x]}")
        return sorted([x for x in manifest if "error" not in x] , key=lambda x: x['filename'])


    # RO property
    @property
    def repo_log(self) -> object:
        return self._log

    @property
    def images_folder_name(self):
        return self._image_parent_name

    def __init__(self, images_name: str):
        """
        :param bom: key to bill of materials
        :type bom: str
        """
        self._log = logging.getLogger(__name__)
        self._image_parent_name = images_name
