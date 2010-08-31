# $Id: $
package PACKAGE_NAME;
use strict;
use base 'CXRi::DB::Cxri2';
use Carp;

# Use CVS Revision as version number.
our $VERSION = sprintf '%d.%03d', q$Revision: 1.4 $ =~ /(\d+)/g;

__PACKAGE__->table('TABLE');
__PACKAGE__->_setup();
__PACKAGE__->set_up_table();
__PACKAGE__->columns( Essential => map {"$_"} __PACKAGE__->columns("All") );

sub _setup {
    my ($class, %args) = @_;
    if ( $args{drop} ) {
        $class->db_Main->do("DROP TABLE IF EXISTS ".$class->table);
    }#END if
    $class->create_table(<<SQL_END);
        `id`                    integer UNSIGNED NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (id)
SQL_END

}#END sub _setup

## sub accessor_name { 
##     my ($class, $column) = @_ ;
##     my %name = ( );
##     return $name{$column} ? $name{$column} : $column 
## }

#----------------------------------------------------------------------
# TRIGGERS
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# PUBLIC METHODS
#----------------------------------------------------------------------

## sub check_values { }#END sub check_values


; "Copyright 2007 Cox Radio Interactive";
__END__

=head1 NAME

PACKAGE_NAME - TBD

=head1 SYNOPSIS

=head1 DESCRIPTION


=head1 COLUMN ACCESSORS

Derived from L<Class::DBI> via L<CXRi::DB::Base>. All columns are accessors.
Unless otherwise noted, all methods CROAK on error.


=head1 CLASS METHODS


=head1 INSTANCE METHODS


=head1 SEE ALSO

L<Class::DBI>, L<CXRi::DB::Base>


=head1 COPYRIGHT

Copyright (C)2007 Cox Radio Interactive 
All rights Reserved

=cut
