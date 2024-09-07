# Changelist Sort
Making Sorting Changelist Files Easy!

1. Close Android Studio (saves changelists to workspace file)
2. Open shell from project root directory (or supply workspace file path in arguments)
3. Run `changelist-sort` (or `cl-sort`) add arguments/options if necessary
4. Reopen Android Studio. Your changelists are sorted.

**Note:** If you want to combine step 2 and step 3, add an alias to your shell environment.

## Sorting By Module
Files are sorted by the name of the top level directory they are located in.
In Android projects, each directory in the project root is a module, with a few special cases.

## Sorting By Source Set
A specialized Module Sort mode that splits changes by their source set.
Apply the `-s` flag to use this sorting mode.

### Special Changelists & Directories
There are special Changelists, and special Directories that are handled differently.
- Build Updates Changelist
- Root Directory
- Gradle Directory

**Build Updates Changelist:**
This is a changelist that is used to collect all of the files that affect the project build.
This includes all files in the gradle directory, and any file that ends with the `.gradle` file extension. There are also Gradle files that end in `.properties`, which are also sorted into the **Build Updates** Changelist.

**Root Directory:**
The Root directory is special because the file paths are really short and do not contain a module name. Often, Root directory contains `.gradle` files which are sorted into the Build Updates Changelist. Any non-Gradle files in the Root directory are sorted into a special Changelist that may be called `Root` or `Project Root`.

**Gradle Directory:**
The Gradle Directory is a direct descendant of the Root directory, and may contain `toml`, `gradle`, or `properties` files. These are all sorted into the **Build Updates** Changelist.

### Module Names and Sorting Comparisons

**Changelist Names**
The name of the changelist must match the module, ignoring letter case and removing spaces.

Otherwise, a new Changelist will be created that matches the module name.
- Underscores are replaced with spaces.
- Each Word in the Name will start with an uppercase letter.

## Remove Empty Changelists
You can remove all empty changelists after a sort has completed by adding the `-r` flag, or `--remove-empty` argument.
