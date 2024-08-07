import pathlib

import pylexibank
from idspy import IDSDataset


class Dataset(IDSDataset):
    dir = pathlib.Path(__file__).parent
    id = "lindseyende"
    writer_options = dict(keep_languages=False, keep_parameters=False)

    # def cmd_download(self, _):
    #     self.raw_dir.xls2csv("ids_cl_ende_final.xlsx")

    def cmd_makecldf(self, args):
        glottocode = "ende1235"
        reprs = ['StandardOrth', 'Phonetic']

        args.writer.add_concepts(id_factory=lambda c: c.attributes['ids_id'])
        args.writer.add_sources(*self.raw_dir.read_bib())

        personnel = self.get_personnel(args)

        args.writer.add_language(
            ID=glottocode,
            Name='Ende (Papua New Guinea)',
            Glottocode=glottocode,
            Authors=personnel['author'],
            DataEntry=personnel['data entry'],
            Consultants=personnel['consultant'],
            Representations=reprs,
            date='2019-10-14',
        )

        for form in pylexibank.progressbar(self.read_csv("ids_cl_ende_final.idsclldorg.csv")):
            if form.form:
                args.writer.add_lexemes(
                    Language_ID=glottocode,
                    Parameter_ID=form.ids_id,
                    Value=form.form,
                    Comment=form.comment,
                    Source="lindsey2019",
                    Transcriptions=reprs,
                    AlternativeValues=form.alt_forms,
                )

        self.apply_cldf_defaults(args)
