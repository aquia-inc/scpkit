from .util import create_session, create_client


def validate_policies(scps, profile, outdir=None, console=False):
    """Validates SCPs 

    Args:
        scps (list of objects): SCP objects  
        profile (object): AWS profile name
    """
    access_analyzer = create_client(create_session(profile), "accessanalyzer")

    for scp in scps:
        if(console):
            print(f"🧪 Validate SCP: {scp.name}")
        scp.validate(access_analyzer)
        if scp.findings:
            if(console):
                print(f"    🚨 Error(s) in {scp.name}:")
                for finding in scp.findings:
                    print(f"       {finding['issueCode']} - {finding['findingDetails']}")
            if outdir:
                scp.write_findings_for_scp(outdir)
                if(console):
                    print(f"    ℹ️  More details check log file {outdir}/{scp.name}-findings.json")
            else:
                print(scp.findings_json)
                if(console):
                    print(f"   ℹ️  More details check log file ./{scp.name}-findings.json")