#!/usr/bin/perl
# Reads the output confusion network (a restricted variant of lattice) from
# spell.py and produces fsal, an openfst-like but line-oriented format. Use the
# trivial script moses/scripts/generic/fsal2fsa.pl to get the standard fsa.
# Ondrej Bojar, bojar@ufal.mff.cuni.cz

use strict;
use Getopt::Long;

my $use_features = undef;
GetOptions(
  "features=s" => \$use_features, # use only the listed features
) or exit 1;

my @use_features; # which features in which order should we emit
if (defined $use_features) {
  @use_features = split /,/, $use_features;
  print STDERR "Using these arc features: $use_features\n";
}
  

my $nr = 0;
while (1) {
  $_ = <>; $nr++;
  last if !defined $_; # end of input
  chomp;
  my ($nvert, $narcs) = split / /;
  my @outarcs = ();
  for my $n (0..$nvert-1) {
    $_ = <>; $nr++;
    die "$nr:Unexpected end of file when reading node $n."
      if !defined $_;
    chomp;
    my $nopts = $_;
    for my $opt (1..$nopts) {
      $_ = <>; $nr++;
      die "$nr:Unexpected end of file when reading option $opt for node $n."
        if !defined $_;
      chomp;
      if (/^\[(\d+)\] (.*?) \|\|\| *(.*)$/) {
        my ($srcnode, $arclabel, $scores) = ($1, $2, $3);
        die "$nr:Undefined source node $srcnode" if $srcnode >= $n;
        if (!defined $use_features && $n>0) {
          # learn to emit all features
          @use_features = map { s/=.*//g; $_ } split / /, $scores;
          $use_features = join(",", @use_features);
          print STDERR "Using these arc features: $use_features\n";
        }
        if ($arclabel eq "</s>" && $scores eq "") {
          # final node
        } else {
          my %scores = split /[ =]/, $scores;
          my @outscores = ();
          foreach my $f (@use_features) {
            my $val = $scores{$f};
            die "$nr:Missing arc feature $f" if !defined $val;
            push @outscores, $val;
          }
          my $outscores = join(",", @outscores);
          push @outarcs, join("|||", ($srcnode, $n, $arclabel, $outscores));
        }
      } elsif ($_ =~ /^<s> \|\|\|\s*$/) {
        # start node, no arc to create
      } else {
        die "$nr:Bad line format: $_"
      }
    }
  }
  print join(" ", @outarcs);
  print "\n";
}

