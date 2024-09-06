"""PeakRDL Docx plug-in."""

__authors__ = ["Alex Nijmeijer <alex.nijmeijer at neads.nl>"]

from typing import TYPE_CHECKING

from peakrdl.plugins.exporter import ExporterSubcommandPlugin    #pylint: disable=import-error
from peakrdl.config import schema                                #pylint: disable=import-error

from .exporter import DocxExporter

if TYPE_CHECKING:
    import argparse
    from typing import Union

    from systemrdl.node import AddrmapNode, RootNode  # type: ignore

class DocxExporterDescriptor(ExporterSubcommandPlugin):  # pylint: disable=too-few-public-methods
    """PeakRDL Docx exporter plug-in."""

    short_desc = "Generate Docx documentation"
    long_desc = "Export the register model to Docx"

    DefaultTableStyle     = "Light Grid Accent 1"
    DefaultListStyle      = "List Bullet"
    DefaultParagraphStyle = "Normal"
    DefaultTitleStyle     = "Title"

    cfg_schema = {
      "TableStyle": schema.String(),
      "ParagraphStyle": schema.String(),
      "ListStyle": schema.String(),
      "TitleStyle": schema.String(),
    }

    def add_exporter_arguments(self, arg_group: "argparse._ActionsContainer"):  # type: ignore
        """Add PeakRDL exporter arguments."""

        arg_group.add_argument(
            "--title",
            dest="title",
            default=None,
            help="Override title text"
        )

        arg_group.add_argument(
            "--depth",
            dest="depth",
            default=0,
            type=int,
            help="Depth of generation (0 means all)",
        )

    def do_export(
        self, top_node: "Union[AddrmapNode, RootNode]", options: "argparse.Namespace"
    ):
        """Perform the export of SystemRDL node to Docx.

        Arguments:
            top_node -- top node to export.
            options -- argparse options from the `peakrdl` tool.
        """

        if self.cfg['TableStyle'] is None :
            self.cfg['TableStyle'] = self.DefaultTableStyle

        if self.cfg['ParagraphStyle'] is None :
            self.cfg['ParagraphStyle'] = self.DefaultParagraphStyle

        if self.cfg['ListStyle'] is None :
            self.cfg['ListStyle'] = self.DefaultListStyle

        if self.cfg['TitleStyle'] is None :
            self.cfg['TitleStyle'] = self.DefaultTitleStyle

        Docx = DocxExporter(
            TableStyle=self.cfg['TableStyle'],
            ParagraphStyle = self.cfg['ParagraphStyle'],
            ListStyle = self.cfg['ListStyle'],
            TitleStyle = self.cfg['TitleStyle']
        )

        Docx.export(
            top_node,
            options.output,
            title=options.title,
            input_files=options.input_files,
        )
