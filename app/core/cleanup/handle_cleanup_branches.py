# app/core/cleanup/handle_cleanup_branches.py


from app.core.cleanup import BranchCleaner

class HandleCleanupBranches:
    def __init__(self, args):
        self.args = args
        self.branchCleaner = BranchCleaner(
            prefix=args.prefix,
            merged_only=args.merged_only,
            older_than=args.older_than,
        )

    def clean(self):
        self.branchCleaner.clean()

def handleCleanupBranches(args) -> HandleCleanupBranches:
    return HandleCleanupBranches(args=args)
