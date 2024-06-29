{
  config,
  lib,
  pkgs,
  ...
}: {
  services.sshd.enable = true;

  users.users.root.password = "nixos";

  users.users.alex = {
    isNormalUser = true;
    home = "/home/alex";
    openssh.authorizedKeys.keys = [ "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAsmNM+izEWl/tIRncLIc9UFHwjL4b64VGD9ZTqeR/fEbfrhUjcQNmwHMbfF3l35OEFnPw6Afm8TzL/RwM+ePpdxj7HzZW6XBOVf258Dcs3olw/JuG8+oSvLoXUiTS1rqgNNp7RLEQN1IxYOUCreu6ju6y2WDi8Ota2vO1DpGgfHB1M6KbGBpLpZBCAKzrhI9I0y6nx6WEWWYJpcvN947oAgQRf/Bv4j9pNUATXhe14rNSWwk5lvOYZSEu7XZeg55GSzJSQjIO29F2SW8b886pB3hbRV+OFtLwWaMvsQwNp25n4wePQJX5OczKZxbN6rfjf4kuOmeGbVP3PmHa8hrmEw== alex@case" ];
  };

  services.openssh.settings.PermitRootLogin = lib.mkDefault "yes";
  services.getty.autologinUser = lib.mkDefault "root";
}
