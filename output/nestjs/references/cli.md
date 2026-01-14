# Nestjs - Cli

**Pages:** 4

---

## 

**URL:** https://docs.nestjs.com/cli/usages

**Contents:**
  - CLI command reference
    - nest new#
      - Description
      - Arguments
      - Options
    - nest generate#
      - Arguments
      - Schematics
      - Options
    - nest build#

Creates a new (standard mode) Nest project.

Creates and initializes a new Nest project. Prompts for package manager.

Generates and/or modifies files based on a schematic

Compiles an application or workspace into an output folder.

Also, the build command is responsible for:

Compiles and runs an application (or default project in a workspace).

Imports a library that has been packaged as a nest library, running its install schematic.

Displays information about installed nest packages and other helpful system info. For example:

**Examples:**

Example 1 (bash):
```bash
$ nest new <name> [options]
$ nest n <name> [options]
```

Example 2 (bash):
```bash
$ nest generate <schematic> <name> [options]
$ nest g <schematic> <name> [options]
```

Example 3 (bash):
```bash
$ nest build <name> [options]
```

Example 4 (bash):
```bash
$ nest start <name> [options]
```

---

## 

**URL:** https://docs.nestjs.com/cli/workspaces

**Contents:**
  - Workspaces
    - Standard mode#
    - Monorepo mode#
    - Workspace projects#
    - Applications#
    - Libraries#
    - CLI properties#
    - Global compiler options#
    - Global generate options#
    - Project-specific generate options#

Nest has two modes for organizing code:

It's important to note that virtually all of Nest's features are independent of your code organization mode. The only effect of this choice is how your projects are composed and how build artifacts are generated. All other functionality, from the CLI to core modules to add-on modules work the same in either mode.

Also, you can easily switch from standard mode to monorepo mode at any time, so you can delay this decision until the benefits of one or the other approach become more clear.

When you run nest new, a new project is created for you using a built-in schematic. Nest does the following:

From there, you can modify the starter files, add new components, add dependencies (e.g., npm install), and otherwise develop your application as covered in the rest of this documentation.

To enable monorepo mode, you start with a standard mode structure, and add projects. A project can be a full application (which you add to the workspace with the command nest generate app) or a library (which you add to the workspace with the command nest generate library). We'll discuss the details of these specific types of project components below. The key point to note now is that it is the act of adding a project to an existing standard mode structure that converts it to monorepo mode. Let's look at an example.

We've constructed a standard mode structure, with a folder structure that looks like this:

We can convert this to a monorepo mode structure as follows:

At this point, nest converts the existing structure to a monorepo mode structure. This results in a few important changes. The folder structure now looks like this:

The generate app schematic has reorganized the code - moving each application project under the apps folder, and adding a project-specific tsconfig.app.json file in each project's root folder. Our original my-project app has become the default project for the monorepo, and is now a peer with the just-added my-app, located under the apps folder. We'll cover default projects below.

A monorepo uses the concept of a workspace to manage its member entities. Workspaces are composed of projects. A project may be either:

All workspaces have a default project (which should be an application-type project). This is defined by the top-level "root" property in the nest-cli.json file, which points at the root of the default project (see CLI properties below for more details). Usually, this is the standard mode application you started with, and later converted to a monorepo using nest generate app. When you follow these steps, this property is populated automatically.

Default projects are used by nest commands like nest build and nest start when a project name is not supplied.

For example, in the above monorepo structure, running

will start up the my-project app. To start my-app, we'd use:

Application-type projects, or what we might informally refer to as just "applications", are complete Nest applications that you can run and deploy. You generate an application-type project with nest generate app.

This command automatically generates a project skeleton, including the standard src and test folders from the typescript starter. Unlike standard mode, an application project in a monorepo does not have any of the package dependency (package.json) or other project configuration artifacts like .prettierrc and eslint.config.mjs. Instead, the monorepo-wide dependencies and config files are used.

However, the schematic does generate a project-specific tsconfig.app.json file in the root folder of the project. This config file automatically sets appropriate build options, including setting the compilation output folder properly. The file extends the top-level (monorepo) tsconfig.json file, so you can manage global settings monorepo-wide, but override them if needed at the project level.

As mentioned, library-type projects, or simply "libraries", are packages of Nest components that need to be composed into applications in order to run. You generate a library-type project with nest generate library. Deciding what belongs in a library is an architectural design decision. We discuss libraries in depth in the libraries chapter.

Nest keeps the metadata needed to organize, build and deploy both standard and monorepo structured projects in the nest-cli.json file. Nest automatically adds to and updates this file as you add projects, so you usually do not have to think about it or edit its contents. However, there are some settings you may want to change manually, so it's helpful to have an overview understanding of the file.

After running the steps above to create a monorepo, our nest-cli.json file looks like this:

The file is divided into sections:

The top-level properties are as follows:

These properties specify the compiler to use as well as various options that affect any compilation step, whether as part of nest build or nest start, and regardless of the compiler, whether tsc or webpack.

These properties specify the default generate options to be used by the nest generate command.

The following example uses a boolean value to specify that spec file generation should be disabled by default for all projects:

The following example uses a boolean value to specify flat file generation should be the default for all projects:

In the following example, spec file generation is disabled only for service schematics (e.g., nest generate service...):

In addition to providing global generate options, you may also specify project-specific generate options. The project specific generate options follow the exact same format as the global generate options, but are specified directly on each project.

Project-specific generate options override global generate options.

The reason for the different default compilers is that for larger projects (e.g., more typical in a monorepo) webpack can have significant advantages in build times and in producing a single file bundling all project components together. If you wish to generate individual files, set "webpack" to false, which will cause the build process to use tsc (or swc).

The webpack options file can contain standard webpack configuration options. For example, to tell webpack to bundle node_modules (which are excluded by default), add the following to webpack.config.js:

Since the webpack config file is a JavaScript file, you can even expose a function that takes default options and returns a modified object:

TypeScript compilation automatically distributes compiler output (.js and .d.ts files) to the specified output directory. It can also be convenient to distribute non-TypeScript files, such as .graphql files, images, .html files and other assets. This allows you to treat nest build (and any initial compilation step) as a lightweight development build step, where you may be editing non-TypeScript files and iteratively compiling and testing. The assets should be located in the src folder otherwise they will not be copied.

The value of the assets key should be an array of elements specifying the files to be distributed. The elements can be simple strings with glob-like file specs, for example:

For finer control, the elements can be objects with the following keys:

This element exists only for monorepo-mode structures. You generally should not edit these properties, as they are used by Nest to locate projects and their configuration options within the monorepo.

**Examples:**

Example 1 (bash):
```bash
$ nest new my-project
```

Example 2 (bash):
```bash
$ cd my-project
$ nest generate app my-app
```

Example 3 (bash):
```bash
$ nest start
```

Example 4 (bash):
```bash
$ nest start my-app
```

---

## 

**URL:** https://docs.nestjs.com/cli/scripts

**Contents:**
  - Nest CLI and scripts
    - The nest binary#
    - Build#
    - Execution#
    - Generation#
    - Package scripts#
    - Backward compatibility#
    - Migration#

This section provides additional background on how the nest command interacts with compilers and scripts to help DevOps personnel manage the development environment.

A Nest application is a standard TypeScript application that needs to be compiled to JavaScript before it can be executed. There are various ways to accomplish the compilation step, and developers/teams are free to choose a way that works best for them. With that in mind, Nest provides a set of tools out-of-the-box that seek to do the following:

This goal is accomplished through a combination of the nest command, a locally installed TypeScript compiler, and package.json scripts. We describe how these technologies work together below. This should help you understand what's happening at each step of the build/execute process, and how to customize that behavior if necessary.

The nest command is an OS level binary (i.e., runs from the OS command line). This command actually encompasses 3 distinct areas, described below. We recommend that you run the build (nest build) and execution (nest start) sub-commands via the package.json scripts provided automatically when a project is scaffolded (see typescript starter if you wish to start by cloning a repo, instead of running nest new).

nest build is a wrapper on top of the standard tsc compiler or swc compiler (for standard projects) or the webpack bundler using the ts-loader (for monorepos). It does not add any other compilation features or steps except for handling tsconfig-paths out of the box. The reason it exists is that most developers, especially when starting out with Nest, do not need to adjust compiler options (e.g., tsconfig.json file) which can sometimes be tricky.

See the nest build documentation for more details.

nest start simply ensures the project has been built (same as nest build), then invokes the node command in a portable, easy way to execute the compiled application. As with builds, you are free to customize this process as needed, either using the nest start command and its options, or completely replacing it. The entire process is a standard TypeScript application build and execute pipeline, and you are free to manage the process as such.

See the nest start documentation for more details.

The nest generate commands, as the name implies, generate new Nest projects, or components within them.

Running the nest commands at the OS command level requires that the nest binary be installed globally. This is a standard feature of npm, and outside of Nest's direct control. One consequence of this is that the globally installed nest binary is not managed as a project dependency in package.json. For example, two different developers can be running two different versions of the nest binary. The standard solution for this is to use package scripts so that you can treat the tools used in the build and execute steps as development dependencies.

When you run nest new, or clone the typescript starter, Nest populates the new project's package.json scripts with commands like build and start. It also installs the underlying compiler tools (such as typescript) as dev dependencies.

You run the build and execute scripts with commands like:

These commands use npm's script running capabilities to execute nest build or nest start using the locally installednest binary. By using these built-in package scripts, you have full dependency management over the Nest CLI commands*. This means that, by following this recommended usage, all members of your organization can be assured of running the same version of the commands.

*This applies to the build and start commands. The nest new and nest generate commands aren't part of the build/execute pipeline, so they operate in a different context, and do not come with built-in package.json scripts.

For most developers/teams, it is recommended to utilize the package scripts for building and executing their Nest projects. You can fully customize the behavior of these scripts via their options (--path, --webpack, --webpackPath) and/or customize the tsc or webpack compiler options files (e.g., tsconfig.json) as needed. You are also free to run a completely custom build process to compile the TypeScript (or even to execute TypeScript directly with ts-node).

Because Nest applications are pure TypeScript applications, previous versions of the Nest build/execute scripts will continue to operate. You are not required to upgrade them. You can choose to take advantage of the new nest build and nest start commands when you are ready, or continue running previous or customized scripts.

While you are not required to make any changes, you may want to migrate to using the new CLI commands instead of using tools such as tsc-watch or ts-node. In this case, simply install the latest version of the @nestjs/cli, both globally and locally:

You can then replace the scripts defined in package.json with the following ones:

**Examples:**

Example 1 (bash):
```bash
$ npm run build
```

Example 2 (bash):
```bash
$ npm run start
```

Example 3 (bash):
```bash
$ npm install -g @nestjs/cli
$ cd  /some/project/root/folder
$ npm install -D @nestjs/cli
```

Example 4 (typescript):
```typescript
"build": "nest build",
"start": "nest start",
"start:dev": "nest start --watch",
"start:debug": "nest start --debug --watch",
```

---

## 

**URL:** https://docs.nestjs.com/cli/libraries

**Contents:**
  - Libraries
    - Nest libraries#
    - Creating libraries#
    - Using libraries#

Many applications need to solve the same general problems, or re-use a modular component in several different contexts. Nest has a few ways of addressing this, but each works at a different level to solve the problem in a way that helps meet different architectural and organizational objectives.

Nest modules are useful for providing an execution context that enables sharing components within a single application. Modules can also be packaged with npm to create a reusable library that can be installed in different projects. This can be an effective way to distribute configurable, re-usable libraries that can be used by different, loosely connected or unaffiliated organizations (e.g., by distributing/installing 3rd party libraries).

For sharing code within closely organized groups (e.g., within company/project boundaries), it can be useful to have a more lightweight approach to sharing components. Monorepos have arisen as a construct to enable that, and within a monorepo, a library provides a way to share code in an easy, lightweight fashion. In a Nest monorepo, using libraries enables easy assembly of applications that share components. In fact, this encourages decomposition of monolithic applications and development processes to focus on building and composing modular components.

A Nest library is a Nest project that differs from an application in that it cannot run on its own. A library must be imported into a containing application in order for its code to execute. The built-in support for libraries described in this section is only available for monorepos (standard mode projects can achieve similar functionality using npm packages).

For example, an organization may develop an AuthModule that manages authentication by implementing company policies that govern all internal applications. Rather than build that module separately for each application, or physically packaging the code with npm and requiring each project to install it, a monorepo can define this module as a library. When organized this way, all consumers of the library module can see an up-to-date version of the AuthModule as it is committed. This can have significant benefits for coordinating component development and assembly, and simplifying end-to-end testing.

Any functionality that is suitable for re-use is a candidate for being managed as a library. Deciding what should be a library, and what should be part of an application, is an architectural design decision. Creating libraries involves more than simply copying code from an existing application to a new library. When packaged as a library, the library code must be decoupled from the application. This may require more time up front and force some design decisions that you may not face with more tightly coupled code. But this additional effort can pay off when the library can be used to enable more rapid application assembly across multiple applications.

To get started with creating a library, run the following command:

When you run the command, the library schematic prompts you for a prefix (AKA alias) for the library:

This creates a new project in your workspace called my-library. A library-type project, like an application-type project, is generated into a named folder using a schematic. Libraries are managed under the libs folder of the monorepo root. Nest creates the libs folder the first time a library is created.

The files generated for a library are slightly different from those generated for an application. Here is the contents of the libs folder after executing the command above:

The nest-cli.json file will have a new entry for the library under the "projects" key:

There are two differences in nest-cli.json metadata between libraries and applications:

These differences key the build process to handle libraries appropriately. For example, a library exports its functions through the index.js file.

As with application-type projects, libraries each have their own tsconfig.lib.json file that extends the root (monorepo-wide) tsconfig.json file. You can modify this file, if necessary, to provide library-specific compiler options.

You can build the library with the CLI command:

With the automatically generated configuration files in place, using libraries is straightforward. How would we import MyLibraryService from the my-library library into the my-project application?

First, note that using library modules is the same as using any other Nest module. What the monorepo does is manage paths in a way that importing libraries and generating builds is now transparent. To use MyLibraryService, we need to import its declaring module. We can modify my-project/src/app.module.ts as follows to import MyLibraryModule.

Notice above that we've used a path alias of @app in the ES module import line, which was the prefix we supplied with the nest g library command above. Under the covers, Nest handles this through tsconfig path mapping. When adding a library, Nest updates the global (monorepo) tsconfig.json file's "paths" key like this:

So, in a nutshell, the combination of the monorepo and library features has made it easy and intuitive to include library modules into applications.

This same mechanism enables building and deploying applications that compose libraries. Once you've imported the MyLibraryModule, running nest build handles all the module resolution automatically and bundles the app along with any library dependencies, for deployment. The default compiler for a monorepo is webpack, so the resulting distribution file is a single file that bundles all of the transpiled JavaScript files into a single file. You can also switch to tsc as described here.

**Examples:**

Example 1 (bash):
```bash
$ nest g library my-library
```

Example 2 (bash):
```bash
What prefix would you like to use for the library (default: @app)?
```

Example 3 (javascript):
```javascript
...
{
    "my-library": {
      "type": "library",
      "root": "libs/my-library",
      "entryFile": "index",
      "sourceRoot": "libs/my-library/src",
      "compilerOptions": {
        "tsConfigPath": "libs/my-library/tsconfig.lib.json"
      }
}
...
```

Example 4 (bash):
```bash
$ nest build my-library
```

---
