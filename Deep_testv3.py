def create_table_on_drawing(self, selected_points, origin, orientation):
    try:
        work_part = self.theSession.Parts.Work
        annotations = work_part.Annotations

        # Tablo satırlarını oluştur
        lines = []
        lines.append("No\tX\tY\tZ")

        for i, p in enumerate(selected_points, start=1):
            pt = self.transform_point(p.Coordinates, origin, orientation)
            line = f"{i}\t{pt.X:.3f}\t{pt.Y:.3f}\t{pt.Z:.3f}"
            lines.append(line)

        final_text = "\n".join(lines)

        # -------- NX12 UYGUN BUILDER --------
        note_builder = annotations.SimpleNoteBuilder(annotations.NewNoteObject())

        note_builder.Text = final_text

        # NOTE konumu
        note_builder.Origin = NXOpen.Point3d(100, 150, 0)

        # NOTU oluştur
        note = note_builder.Commit()
        note_builder.Destroy()

        self.theUI.NXMessageBox.Show(
            "Bilgi",
            NXOpen.NXMessageBox.DialogType.Information,
            "Tablo NOTE olarak çizime eklendi (NX12 uyumlu)."
        )

    except Exception as ex:
        self.theUI.NXMessageBox.Show("Hata", NXOpen.NXMessageBox.DialogType.Error, str(ex))
