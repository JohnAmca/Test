def create_table_on_drawing(self, selected_points, origin, orientation):
    try:
        work_part = self.theSession.Parts.Work
        drafting_body = work_part
        annotations = work_part.Annotations

        # Tabloyu yazacağımız text buffer
        lines = []

        # Başlık
        lines.append("No\tX\tY\tZ")

        # Her nokta için satır ekle
        for i, p in enumerate(selected_points, start=1):
            pt = self.transform_point(p.Coordinates, origin, orientation)
            line = f"{i}\t{pt.X:.3f}\t{pt.Y:.3f}\t{pt.Z:.3f}"
            lines.append(line)

        final_text = "\n".join(lines)

        # NOTE oluşturma builder
        note_builder = annotations.CreateNoteBuilder()

        # Yazı içeriği ayarla
        note_builder.Text.Text = final_text

        # Yazının konulacağı nokta (sheet üzerinde)
        note_origin = NXOpen.Point3d(100.0, 150.0, 0.0)
        note_builder.Origin = note_origin

        # Yatay hizalama
        note_builder.HorizontalAlignment = NXOpen.Annotations.HorizontalAlignment.Left

        # NOTE oluştur
        note_feature = note_builder.Commit()
        note_builder.Destroy()

        self.theUI.NXMessageBox.Show(
            "Bilgi",
            NXOpen.NXMessageBox.DialogType.Information,
            "Tablo çizime NOTE olarak eklendi (NX12 uyumlu)."
        )

    except Exception as ex:
        self.theUI.NXMessageBox.Show("Hata", NXOpen.NXMessageBox.DialogType.Error, str(ex))
