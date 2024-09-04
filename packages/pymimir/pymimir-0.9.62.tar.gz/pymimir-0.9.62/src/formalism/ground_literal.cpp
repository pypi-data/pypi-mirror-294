/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#include "mimir/formalism/ground_literal.hpp"

#include "formatter.hpp"
#include "mimir/formalism/ground_atom.hpp"
#include "mimir/formalism/predicate.hpp"

namespace mimir
{
template<PredicateCategory P>
GroundLiteralImpl<P>::GroundLiteralImpl(Index index, bool is_negated, GroundAtom<P> atom) : m_index(index), m_is_negated(is_negated), m_atom(std::move(atom))
{
}

template<PredicateCategory P>
std::string GroundLiteralImpl<P>::str() const
{
    auto out = std::stringstream();
    out << *this;
    return out.str();
}

template<PredicateCategory P>
Index GroundLiteralImpl<P>::get_index() const
{
    return m_index;
}

template<PredicateCategory P>
bool GroundLiteralImpl<P>::is_negated() const
{
    return m_is_negated;
}

template<PredicateCategory P>
const GroundAtom<P>& GroundLiteralImpl<P>::get_atom() const
{
    return m_atom;
}

template class GroundLiteralImpl<Static>;
template class GroundLiteralImpl<Fluent>;
template class GroundLiteralImpl<Derived>;

template<PredicateCategory P>
std::ostream& operator<<(std::ostream& out, const GroundLiteralImpl<P>& element)
{
    auto formatter = PDDLFormatter();
    formatter.write(element, out);
    return out;
}

template std::ostream& operator<<(std::ostream& out, const GroundLiteralImpl<Static>& element);
template std::ostream& operator<<(std::ostream& out, const GroundLiteralImpl<Fluent>& element);
template std::ostream& operator<<(std::ostream& out, const GroundLiteralImpl<Derived>& element);
}
