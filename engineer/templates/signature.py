import datetime

DATE = str(datetime.date.today())
VERSION = "dev"
NAME = "Arnar Evgeni Gunnarsson"
ORGANIZATION = "Development of Engineering Tools"
EMAIL = "s171950@student.dtu.dk"
SCHOOL = ""
STUDYLINE = "Engineering Design & Applied Mechanics"


def sign(name=NAME, date=DATE, version=VERSION, organization=ORGANIZATION, length=None):
    name =         "Author:\t\t%s" % name
    date    =      "Date:\t\t%s" % date
    version =      "Version:\t%s" % version
    email   =      "Contact:\t%s" % EMAIL
    organization = "%s" % organization
    studyline = "\t%s" % STUDYLINE
    school = "%s" % SCHOOL
    if not length:
        length = max([len(name), len(date), len(version), len(organization), len(email), len(school), len(studyline)]) + 8
    eqs = "=" * length
    mis = "- " * int(length/2) + '-'
    tis = "~" * length
    return"\n".join([mis,
                     name,
                     date,
                     version,
                     email,
                     tis,
                     school,
                     studyline,
                     tis,
                     organization,
                     mis])

def docoptTemplate(progname, description=" ", usage=None):
    if not usage:
        usage = "\n\t".join(["%s --option [--option2] [--varflag <var>] [--verbose] [--debug]" % progname,
                             "%s -h | --help" % progname,
                             "%s -v | --version" % progname])
    options = "\n    ".join(["-h, --help       Shows this help and exits",
                           "-v, --version    Print tool version and exits",
                           "--verbose        Run with lots of information",
                           "--debug          Run in debug mode"])
    length = max([len(i) for i in usage.split('\n')] + [len(i) for i in options.split('\n')] + [len(i) for i in description.split('\n')])
    return """<short>
DESCRIPTION:{description}

USAGE:
    {usage}

OPTIONS:
    {options}

{sign}

""".format(description=description, usage=usage, options=options, sign=sign(length=length))

def scriptTemplate(progname, descripton=" ", usage=None, imports=None):
    if not imports:
        imports = []
    if 'os' not in imports:
        imports.append('os')
    if 'sys' not in imports:
        imports.append('sys')
    imports = "import " + "import\n".join(imports)
    doc = docoptTemplate(progname=progname, description=descripton, usage=usage)

    main_func = "\n\t".join(["if __name__ == '__main__':\n",
                             "if len(sys.argv) == 1:",
                             "\tprint(__doc__)",
                             "\texit(0)"])
    return "\n\n\n".join([imports, doc, main_func])

if __name__ == "__main__":
    print(scriptTemplate("setup_mv.py", imports=['os', 'sys']))
