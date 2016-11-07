def main():
    import os
    import sys
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import apitest
    
    __package__ = str("apitest")
    
    # Run the cmd
    from apitest.actions.sendto.cli import cli
    
    cli()

if __name__ == "__main__":
    main()  # pragma no cover
