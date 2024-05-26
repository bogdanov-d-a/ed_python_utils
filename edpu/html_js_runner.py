def generate(alias: str, dir_path: str) -> None:
    with open(fr'{dir_path}\{alias}.html', 'w', encoding='ascii', newline='') as file:
        file.write('<!DOCTYPE html>\n')
        file.write(f'<script src="{alias}.js"></script>\n')
