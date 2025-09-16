from pathlib import Path


parent = Path(r'C:\Users\Mathsphile\Documents\Projects\PYTHON\AnimeDL\Files\Seasons\Solo.Leveling.Season.2.Arise.From.The.Shadow.Ore.Dake.Level.Up.Na.Ken.Season.2')

for i in range(12):
    fn = parent / \
        f'Solo.Leveling.Season.2.Arise.From.The.Shadow.Ore.Dake.Level.Up.Na.Ken.Season.2.E{i+1:02}.mp4'
    if fn.is_file():
        continue
    fn.touch()
    # new_name = f'Episode {i+1} - {episode_path.stem}.mp4'
    # episode_path.rename(season_path / new_name)
