from metaApp.metaHelper.FileManager import FileManager
from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger, PdfFileReader


class PdfManager(FileManager):
    def get_all_metadata(self):
        pdf_reader = PdfFileReader(self.dir_to_file)
        metadata = pdf_reader.getDocumentInfo()
        return metadata

    def set_property(self, key, value):
        file_in = open(self.dir_to_file, 'rb')
        pdf_reader = PdfFileReader(file_in)
        metadata = pdf_reader.getDocumentInfo()

        pdf_merger = PdfFileMerger()
        pdf_merger.append(file_in)
        pdf_merger.addMetadata({key: value})

        file_out = open(self.dir_to_file, 'wb')
        pdf_merger.write(file_out)

        file_in.close()
        file_out.close()

    def clear_all_data(self):
        pass

    def get_content_type(self):
        return 'application/pdf'
