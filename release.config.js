module.exports = {
    "dryRun": false,
    "plugins": [
      "@semantic-release/commit-analyzer",
      "@semantic-release/release-notes-generator",
      "semantic-release-pypi",
      "@semantic-release/changelog",
      "@semantic-release/github",
      [
        "@semantic-release/git",
        {
          "assets": [
            "CHANGELOG.md",
            "setup.py",
            "setup.cfg"
          ],
          "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
        }
      ]
    ]
  };
  
