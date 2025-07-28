if __name__ == '__main__':
    with open('probe_url_test.txt', 'w', encoding='utf-8') as file:
        def write_probe_url(url: str) -> None:
            from edpu.probe_url import probe_url

            file.write(f'url = <{url}>\n')
            file.write('\n'.join(probe_url(url)) + '\n\n')

        write_probe_url('')
        write_probe_url('4881a8336afd2e9ac3ee503dfed1e8d3cfb3e21e')
        write_probe_url('https://1494a60b15afa03f06039e48f6ad13d661aef1e4')

        write_probe_url('https://www.wikipedia.org/')
        write_probe_url('https://en.wikipedia.org/')
        write_probe_url('https://ru.wikipedia.org/')
        write_probe_url('https://www1.wikipedia.org/')
        write_probe_url('https://en.wikiipedia.org/')

        write_probe_url('https://www.youtube.com/')
        write_probe_url('https://www.youutube.com/')
        write_probe_url('https://www.youtube.comm')

        write_probe_url('https://github.com/')
        write_probe_url('https://github.co')
        write_probe_url('https://githb.com/')

        write_probe_url('https://stackoverflow.com/')
        write_probe_url('https://stackoverflow.comm')
        write_probe_url('https://stuckoverflow.com/')

        write_probe_url('https://pypi.org/')
        write_probe_url('https://pypi.or')
        write_probe_url('https://pypii.org/')
