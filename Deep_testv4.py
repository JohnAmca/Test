def create_table_on_drawing(self, selected_points, origin, orientation):
    try:
        work_part = self.theSession.Parts.Work
        annotations = work_part.Annotations

        # ---- Drafting Sheet’e geç ----
        active_sheet = work_part.DrawingSheets.CurrentDrawingSheet
        work_part.DrawingSheets.SetCurrentDrawingSheet(active_sheet)

        # ---- Tablo yazılarını hazırla ----
        lines = []
        lines.append("No\tX\tY\tZ")

        for i, p in enumerate(selected_points, start=1):
            pt = self.transform_point(p.Coordinates, origin, orientation)
            lines.append(f"{i}\t{pt.X:.3f}\t{pt.Y:.3f}\t{pt.Z:.3f}")

        final_text = "\n".join(lines)

        # ---- NX12 UYUMLU NOTE BUILDER ----
        note_builder = annotations.SimpleNoteBuilder(annotations.NewNoteObject())

        note_builder.Text = final_text

        # NOTE’i sheet üzerine yerleştireceğimiz nokta
        note_builder.Origin = NXOpen.Point3d(50.0, 50.0, 0.0)

        # NOTU OLUŞTUR
        note_obj = note_builder.Commit()
        note_builder.Destroy()

        self.theUI.NXMessageBox.Show(
            "Bilgi",
            NXOpen.NXMessageBox.DialogType.Information,
            "Tablo aktif DRAWING SHEET'e başarıyla eklendi."
        )

    except Exception as ex:
        self.theUI.NXMessageBox.Show(
            "Hata", NXOpen.NXMessageBox.DialogType.Error, str(ex)
        )
