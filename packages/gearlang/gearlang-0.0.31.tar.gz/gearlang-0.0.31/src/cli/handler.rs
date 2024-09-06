use clap::{command, Parser, Subcommand};
use crate::cli::commands;

#[derive(Parser)]
#[clap(about, version, author)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,
}


#[derive(Parser)]
#[clap(name = "build")]
struct BuildCommand {
    #[clap(short, long, alias = "l")]
    lib: bool,
}

#[derive(Parser)]
#[clap(name = "install")]
struct InstallCommand {
    #[clap(short, long)]
    force: bool,
}


#[derive(Subcommand)]
enum Commands {
    Build(BuildCommand),
    Install(InstallCommand),
}



pub fn cli_run() {
    let arg = Cli::parse();


    match &arg.command {
        Commands::Build(build_command) => {
            println!("Building...");

            commands::build::compile(build_command.lib);

        }
        Commands::Install(install_command) => {
            println!("Installing...");

            if install_command.force {
                println!("Force install");
            } else {
                println!("Normal install");
            }
        }
    }


}
