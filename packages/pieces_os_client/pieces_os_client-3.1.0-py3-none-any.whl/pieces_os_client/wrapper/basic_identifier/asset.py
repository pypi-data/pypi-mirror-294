from ..streamed_identifiers.assets_snapshot import AssetSnapshot
from pieces_os_client import (
	Asset, 
	AssetsApi,
	AssetApi,
	ClassificationSpecificEnum,
	FormatApi,
	ClassificationGenericEnum,
	Annotation,
	Format,
	Classification,
	Annotations,
	SeededAsset,
	Seed,
	SeededFormat,
	SeededFragment,
	TransferableString,
	FragmentMetadata,
	AssetReclassification,
	Linkify,
	Shares
)

from typing import Optional
from .basic import Basic
from .user import BasicUser

# Friendly wrapper (to avoid interacting with the pieces_os_client sdks models)

class BasicAsset(Basic):
	"""
	A wrapper class for managing assets.
	"""
		
	@property
	def asset(self) -> Asset:
		asset = AssetSnapshot.identifiers_snapshot.get(self._id)
		if not asset:
			raise ValueError("Asset not found")
		return asset

	@property
	def id(self) -> str:
		"""
			:returns: The asset id
		"""
		return self.asset.id

	@property
	def raw_content(self) -> Optional[str]:
		"""
		Get the raw content of the asset.

		Returns:
			Optional[str]: The raw content if available, otherwise None.

		Raises:
			ValueError: If unable to get OCR content for an image.
		"""
		if self.is_image:
			content = self._get_ocr_content()
			if content is None:
				raise ValueError('Unable to get OCR content')
			return content
		else:
			return (
				self.asset.original.reference.fragment.string.raw or
				self.asset.preview.base.reference.fragment.string.raw or
				''
			)

	@raw_content.setter
	def raw_content(self, content: str):
		"""
		Edit the original format of the asset.

		Args:
			content: The new content to be set.

		Raises:
			NotImplemented: If the asset is an image.
		"""
		format_api = AssetSnapshot.pieces_client.format_api
		original = format_api.format_snapshot(self.asset.original.id, transferable=True)
		if original.classification.generic == ClassificationGenericEnum.IMAGE:
			raise NotImplemented("Can't edit an image yet")

		if original.fragment and original.fragment.string and original.fragment.string.raw:
			original.fragment.string.raw = content
		elif original.file and original.file.string and original.file.string.raw:
			original.file.string.raw = content
		format_api.format_update_value(transferable=False, format=original)

	@property
	def is_image(self) -> bool:
		"""
		Check if the asset is an image.

		Returns:
			bool: True if the asset is an image, otherwise False.
		"""
		return (
			self.asset.original.reference.classification.generic ==
			ClassificationGenericEnum.IMAGE
		)


	@property
	def classification(self) -> Optional[ClassificationSpecificEnum]:
		"""
		Get the specific classification of the asset (eg: py).

		:return: The classification value of the asset, or None if not available.
		"""
		if self.is_image:
			ocr_format = self._get_ocr_format(self.asset)
			if ocr_format:
				return ocr_format.classification.specific
		return self.asset.original.reference.classification.specific

	@classification.setter
	def classification(self, classification):
		"""
		Reclassify the classification attribute.

		Args:
			classification (str or ClassificationSpecificEnum): The new classification value.

		Raises:
			ValueError: If the classification is not a string or ClassificationSpecificEnum.
			NotImplementedError: If the asset is an image, reclassification is not supported.
		"""
		if isinstance(classification, str):
			if classification not in ClassificationSpecificEnum:
				raise ValueError(f"Classification must be one from {list(ClassificationSpecificEnum)}")
			classification = ClassificationSpecificEnum(classification)

		if not isinstance(classification, ClassificationSpecificEnum):
			raise ValueError("Invalid classification")

		if self.is_image:
			raise NotImplementedError("Error in reclassify asset: Image reclassification is not supported")

		AssetSnapshot.pieces_client.asset_api.asset_reclassify(
			asset_reclassification=AssetReclassification(
				ext=classification, asset=self.asset),
			transferables=False
		)



	@property
	def name(self) -> str:
		"""
		Get the name of the asset.

		Returns:
			Optional[str]: The name of the asset if available, otherwise "Unnamed snippet".
		"""
		return self.asset.name if self.asset.name else "Unnamed snippet"
	
	@name.setter
	def name(self, name: str):
		"""
		Edit the name of the asset.

		:param name: The new name to be set for the asset.
		"""
		self.asset.name = name
		self._edit_asset(self.asset)

	@property
	def description(self):
		"""
		Retrieve the description of the asset.

		:return: The description text of the asset, or None if not available.
		"""
		annotations = self.annotations
		if not annotations:
			return
		annotations = sorted(annotations, key=lambda x: x.updated.value, reverse=True)
		d = None
		for annotation in annotations:
			if annotation.type == "DESCRIPTION":
				d = annotation
		
		return d.text if d else None


	@property
	def annotations(self) -> Optional[Annotations]:
		"""
		Get all annotations of the asset.

		Returns:
			Optional[Annotations]: The annotations if available, otherwise None.
		"""
		return getattr(self.asset.annotations,"iterable",None)


	def delete(self):
		"""
		Delete the asset.
		"""
		AssetSnapshot.pieces_client.assets_api.assets_delete_asset(self.id)

	@classmethod
	def create(cls,raw_content: str, metadata: Optional[FragmentMetadata] = None) -> str:
		"""
		Create a new asset.

		Args:
			raw_content (str): The raw content of the asset.
			metadata (Optional[FragmentMetadata]): The metadata of the asset.

		Returns:
			str: The ID of the created asset.
		"""
		seed = cls._get_seed(raw_content,metadata)

		created_asset_id = AssetSnapshot.pieces_client.assets_api.assets_create_new_asset(transferables=False, seed=seed).id
		return created_asset_id

	def share(self) -> Shares:
		"""
		Generates a shareable link for the given asset.

		Raises:
		PermissionError: If the user is not logged in or is not connected to the cloud.
		"""
		return self._share(self.asset)


	@classmethod
	def share_raw_content(cls,raw_content:str) -> Shares:
		"""
		Generates a shareable link for the given user raw content.
		Note: this will create an asset

		Args:
			raw_content (str): The raw content of the asset that will be shared.

		Raises:
		PermissionError: If the user is not logged in or is not connected to the cloud.
		"""
		return cls._share(seed = cls._get_seed(raw_content))

	@staticmethod
	def _get_seed(raw: str, metadata: Optional[FragmentMetadata] = None) -> Seed:
		return Seed(
			asset=SeededAsset(
				application=AssetSnapshot.pieces_client.tracked_application,
				format=SeededFormat(
					fragment=SeededFragment(
						string=TransferableString(raw=raw),
						metadata=metadata
					)
				),
				metadata=None
			),
			type="SEEDED_ASSET"
		)

	def _get_ocr_content(self) -> Optional[str]:
		"""
		Get the OCR content of the asset.

		Returns:
			Optional[str]: The OCR content if available, otherwise None.
		"""
		if not self.asset:
			return
		format = self._get_ocr_format(self.asset)
		if format is None:
			return
		return self._ocr_from_format(format)

	@staticmethod
	def _get_ocr_format(src: Asset) -> Optional[Format]:
		"""
		Get the OCR format of the asset.

		Args:
			src (Asset): The asset object.

		Returns:
			Optional[Format]: The OCR format if available, otherwise None.
		"""
		image_id = src.original.reference.analysis.image.ocr.raw.id if src.original and src.original.reference and src.original.reference.analysis and src.original.reference.analysis.image and src.original.reference.analysis.image.ocr and src.original.reference.analysis.image.ocr.raw and src.original.reference.analysis.image.ocr.raw.id else None
		if image_id is None:
			return None
		return next((element for element in src.formats.iterable if element.id == image_id), None)

	@staticmethod
	def _ocr_from_format(src: Optional[Format]) -> Optional[str]:
		"""
		Extract OCR content from the format.

		Args:
			src (Optional[Format]): The format object.

		Returns:
			Optional[str]: The OCR content if available, otherwise None.
		"""
		if src is None:
			return None
		return bytes(src.file.bytes.raw).decode('utf-8')

	@staticmethod
	def _edit_asset(asset):
		AssetSnapshot.pieces_client.asset_api.asset_update(False,asset)

	@staticmethod
	def _share(asset=None,seed=None):
		"""
			You need to either give the seed or the asset_id
		"""
		if asset:
			kwargs = {"asset" : asset}
		else:
			kwargs = {"seed" : seed}

		user = BasicUser.user_profile

		if not user:
			raise PermissionError("You need to be logged in to generate a shareable link")

		if not user.allocation:
			raise PermissionError("You need to connect to the cloud to generate a shareable link")

		return AssetSnapshot.pieces_client.linkfy_api.linkify(
			linkify=Linkify(
				access="PUBLIC",
				**kwargs
				)
			)
